from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
prism_gateway = gateway.entry_point               # get the AdditionApplication instance

n = 2
initial_state = 0
PplusX = gateway.jvm.java.util.ArrayList()
PplusX.add(.5)
PplusX.add(.5)
PplusX.add(.5)
PplusX.add(.5)
prop = "P=?[F=2 s=1]"

sol = prism_gateway.runPrism(prop, PplusX, n, initial_state)
print(sol)
