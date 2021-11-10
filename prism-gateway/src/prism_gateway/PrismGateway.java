package io.github.lisaoakley.prism_gateway;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

import py4j.GatewayServer;

import parser.State;
import parser.VarList;
import parser.ast.Declaration;
import parser.ast.DeclarationInt;
import parser.ast.DeclarationType;
import parser.ast.Expression;
import parser.type.Type;
import parser.type.TypeInt;
import prism.ModelGenerator;
import prism.ModelType;
import prism.Prism;
import prism.PrismDevNullLog;
import prism.PrismException;
import prism.PrismLangException;
import prism.PrismLog;
import prism.RewardGenerator;
import prism.ModelInfo;
import explicit.Model;
import explicit.DTMCSimple;
import explicit.ModelModelGenerator;

public class PrismGateway {

    public static void main(String[] args) {
        PrismGateway gw = new PrismGateway();
        // gw is now the gateway.entry_point
        GatewayServer server = new GatewayServer(gw);
        System.out.println("Starting Prism Server");
        server.start();
    }

    /***
     * Generate a model for the given (flattened) Markov chain transition matrix and initial State. Then check the model based on the given property.
     * @param property The property to check the DTMC model on.
     * @param pPlusX The DTMC transition matrix, flattened to a vector.
     * @param n The number of states in the DTMC
     * @param initialState The DTMC start state
     * @return
     */
    public Object runPrism(String property, List<Double> pPlusX, int n, int initialState)
    {
        try {
            PrismLog mainLog = new PrismDevNullLog();
            Prism prism = new Prism(mainLog);
            prism.initialise();

            // Create model
            ModelInfo modelInfo = new MyModelInfo(n);
            DTMCSimple model = new DTMCSimple(n);
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    model.setProbability(i, j, pPlusX.get(n*i+j));
                }
            }

            // Construct and set VarList
            VarList vlist = new VarList(modelInfo);
            model.setVarList(vlist);

            // Set States and Initial State
            model.addInitialState(initialState);
            List<State> sList = new ArrayList<State>();
            for (int i = 0; i < n; i++) {
                State state = new State(modelInfo.getNumVars());
                state.setValue(0,i);
                sList.add(state);
            }
            model.setStatesList(sList);

            //Create ModelGenerator
            ModelGenerator modelGen = new ModelModelGenerator(model,modelInfo);

            // Load the model generator into PRISM,
            prism.loadModelGenerator(modelGen);
            Object sol = prism.modelCheck(property).getResult();

            // Close down PRISM
            prism.closeDown();
            return sol;

        } catch (PrismException e) {
            System.out.println("Error: " + e.getMessage());
            System.exit(1);
            return null;
        }
    }

    /***
     * A simple ModelInfo implementation for a DTMC.
     */
    class MyModelInfo implements ModelInfo
    {
        private int n;

        /**
         * Construct ModelInfo
         * @param n State size
         */
        public MyModelInfo(int n)
        {
            this.n = n;
        }

        // Methods for ModelInfo interface

        // The model is a discrete-time Markov chain (DTMC)

        @Override
        public ModelType getModelType()
        {
            return ModelType.DTMC;
        }

        // The model's state comprises one, integer-valued variable x with values 0,...,n-1

        @Override
        public List<String> getVarNames()
        {
            return Arrays.asList("s");
        }

        @Override
        public List<Type> getVarTypes()
        {
            return Arrays.asList(TypeInt.getInstance());
        }

        @Override
        public DeclarationType getVarDeclarationType(int i)
        {
            // i will always be 0 since there there is only one variable x
            return new DeclarationInt(Expression.Int(0), Expression.Int(n));
        }

        // There is one label: 'goal'
        @Override
        public List<String> getLabelNames()
        {
            return Arrays.asList("goal");
        }
    }

}
