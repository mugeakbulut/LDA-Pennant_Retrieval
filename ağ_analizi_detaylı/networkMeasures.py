import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def subjectsdisply(subjects,deg,degsor,citingDic):
    #the average degree value for each subject in the dataset.
    print("\nHer bir konu için average degree centrality skoru")
    for sub in subjects:
        lis = []
        for d in degsor:
            if(sub == citingDic[d]):
                lis.append(deg[d])
        print('{0:<40}'.format(sub), '{0:<6}'.format(sum(lis)/len(lis)))

def computecentralities(data):
    G=nx.from_pandas_edgelist(data, 'citingDoc', 'citedDoc', ['citingDocSubj', 'citedDocSubj'])

    citingNodes= list(set(data['citingDoc']))
    citedNode = list(set(data['citedDoc']))
    for value in citedNode:
        if value not in citingNodes:
            citingNodes.append(value)

    citingDic = {}
    print(len(citingNodes))
    for node in citingNodes:
        for i in range(0,len(data)):
            if(node == data.citingDoc[i]):
                citingDic[node] = data.citingDocSubj[i]
                break
            elif(node == data.citedDoc[i]):
                citingDic[node] = data.citedDocSubj[i]
                break
    #basic information of the network
    print(nx.info(G))
    
    subjects=set(citingDic.values())

    #basic visualization of the network
    def visualization(G, ls,nodesize,nodelables=None):
        edges= G.edges()
        pos = nx.spring_layout(G, scale=1)
        nx.draw_networkx_nodes(G, pos,nodelist=ls ,cmap=plt.get_cmap('jet'), node_size = nodesize)
        nx.draw_networkx_labels(G, pos, nodelables)
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='r')
        plt.show()

    visualization(G,G.nodes(),10)


    #fucntion to show top 10 most central nodes in the network
    def top(centralityVlaue, number):
        Deg_sorted_keys = sorted(centralityVlaue, key=centralityVlaue.get, reverse=True)
        i = 0
        #sorting only keys of the dictionary words having degree centrality
        lis=[]
        for dg in Deg_sorted_keys:
            if i < number:
                print('{0:<20}'.format(dg),'{0:<50}'.format(citingDic[dg]),'{0:<6}'.format(centralityVlaue[dg]))
                lis.append(dg)
            i+=1
        return lis,Deg_sorted_keys

    #computing different centrality measures for the articles

    #degree cenrtality measures for graph
    print("\nDegree centrality skorları\n")
    print('{0:<20}'.format("DocID"),'{0:<50}'.format("Konu"),'{0:<6}'.format("Degree centrality"))
    deg = nx.degree_centrality(G)
    ls, degsor=top(deg,20)
    
    subjectsdisply(subjects, deg, degsor,citingDic)


    #visualization(sb,ls,nodesize,nodelables)
    #print("\nLeast 10 nodes using degree centrality")
    #least(deg)

    #betweeness cenrtality measures for graph
    print("\nBetweeness centrality skorları\n")
    print('{0:<20}'.format("DocID"),'{0:<50}'.format("Konu"),'{0:<6}'.format("Betweeness centrality"))
    bet = nx.betweenness_centrality(G)
    ls, betsor=top(bet,20)

    subjectsdisply(subjects, bet, betsor,citingDic)

    #closeness centrality
    print("\nCloseness centrality skorları\n")
    print('{0:<20}'.format("DocID"),'{0:<50}'.format("Konu"),'{0:<6}'.format("Closeness centrality"))
    closeness = nx.closeness_centrality(G)
    ls, closSor=top(closeness,20)

    subjectsdisply(subjects, closeness, closSor,citingDic)

    #pagerank centrality measure
    print("\nPageRank skoruna da bakayım\n")
    print('{0:<20}'.format("DocID"),'{0:<50}'.format("Konu"),'{0:<6}'.format("Pagerank"))
    prank = nx.pagerank(G)
    ls, prankSor=top(prank,20)

    subjectsdisply(subjects, prank, prankSor,citingDic)
