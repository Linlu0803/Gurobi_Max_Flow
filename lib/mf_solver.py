import gurobipy as gp
from gurobipy import GRB

def solve_mf (nodes, arcs, source, sink):
    model = gp.Model("max_flow")

    # create variable for flow : 0<flow< capacity(lb: lower bound, ub: upper bound, name: from i to j)
    flow = {}
    for arc in arcs:
        flow[arc['start'], arc['end']] = model.addVar(
            lb=0, ub=arc['capacity'], name=f"flow_{arc['start']}_{arc['end']}")

    #constraints        
    for node in nodes:
        if node == source:
                
            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == node) == 0,
                name=f"flow_balance_{node}_in")
                #sum of flow in = 0

        elif node == sink:

            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['start'] == node) == 0,
                name=f"flow_balance_{node}_out")
            #for sink: sum of flow out =0
        else:
            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == node) ==
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['start'] == node),
                name=f"flow_balance_{node}")
    
    # Set objective
    model.setObjective(
        gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == sink),
        GRB.MAXIMIZE)
    #Optimize beginn
    model.optimize()


    if model.status == GRB.OPTIMAL: #GRB.OPTIMAL =" the optimization was successful"
        max_flow = model.objVal
        flow_values = {arc: flow[arc].X for arc in flow}
                        #  flow[arc].X = flow value of each arc
        return max_flow, flow_values
    else:
        raise Exception("No optimal solution found")
    