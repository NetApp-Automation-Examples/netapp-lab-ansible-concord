sequential_nodes_list = [];

//loop through ha_pairs and set i to 0 for each cluster
for (const cluster of ha_pairs.keySet()) {
    pairs_list = ha_pairs.get(cluster);
    i = 0;

    pairs_list.forEach(function(pair){

        pair.forEach(function(node){
            // if we don't have an array at the current index yet, create an empty one
            if(typeof sequential_nodes_list[i] === 'undefined') {
                sequential_nodes_list[i] = {}
            } 

            // create a cluster:node object and insert into the current index
            // obj = {};
            // obj[cluster]=node;
            
            sequential_nodes_list[i][cluster]=node //.push(obj);
            
            // iterate i to get proper array index 
            i++;
        });
    });
}

// return variable to concord
execution.variables().set('sequential_nodes_list', sequential_nodes_list);
