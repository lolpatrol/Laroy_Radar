import graphviz


colors = {
    "todo": 'gray',
    "doing": 'yellow',
    "done": 'green'
}


def get_nodes():
    nodes = {}
    files = ["todo", "doing", "done"]
    for file in files:
        nodes[file] = []
        f = open(file).read().splitlines()
        for line in f:
            name, type, r = line.split(":")
            if len(r) >= 1 and r[0] != "-":
                r = r.split(",")
            else:
                r = []
            nodes[file].append((name, type, r))
    return nodes


g = graphviz.Digraph("G", engine='fdp')  # circo => nice circular thingy
g.attr(rankdir='LR', size='12')
nodes = get_nodes()
reasons = set()

with g.subgraph(name="cluster_todo") as c:
    c.attr(color='gray')
    c.node_attr.update(style='filled', color='gray')
    for node in nodes["todo"]:
        n, t, r = node
        if len(r) > 0:
            for re in r:
                reasons.add((re, n))
        c.node(n)
    c.attr(label='TODO')  # No labels with engine='circo', also subgraphs don't seem to work here either (to collect)

with g.subgraph(name='cluster_doing') as d:
    d.attr(color='blue')
    d.node_attr.update(style='filled', color='yellow')
    for node in nodes["doing"]:
        n, t, r = node
        if len(r) > 0:
            for re in r:
                reasons.add((re, n))
        d.node(n)
    d.attr(label='Doing')

with g.subgraph(name="cluster_done") as e:
    e.attr(color='green')
    e.node_attr.update(style='filled', color='green')
    for node in nodes["done"]:
        n, t, r = node
        if len(r) > 0:
            for re in r:
                g.node(re, shape='rectangle')
                e.edges([(re, n)])
        else:
            e.node(n)
    if len(nodes["done"]) == 0:
        e.node(":(")
    e.attr(label='Done')

r = list(set([p[0] for p in reasons]))
for item in r:
    g.node(item, style='filled', shape='rectangular', color='orange')
for i in range(len(r)-1):
        g.edge(r[i], r[i+1], style='invis', rank='same')
for pair in reasons:
    g.edge(pair[0], pair[1])

g.render(filename='laroy_radar', format='png')
g.view()

