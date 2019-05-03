# | :---: | --- | :---: |
# |   6   |  1  |   5   |
# |   0   |  2  |   4   |
# |   7   |  3  |   8   |
          
  # following table is result table, after calling agent.astar()

# | :---: | --- | :---: |
# |   0   |  1  |   2   |
# |   3   |  4  |   5   |
# |   6   |  7  |   8   |

class agent:    
    def __init__(self, initial_state):
        self.goal_state=[0,1,2,3,4,5,6,7,8]
        self.graph={0:{'depth':0, 'state':initial_state,'parent':None,'cost':0}}
        self.n_node=0                    
        self.fringe=[0]
        self.visited=[]
        self.solution=None
        self.finished=False

    def swap_element(self,state,direction):

        temp=state[:]
        swap_index=None

        index_dir = {
            0:[1,3], 
            1:[0,2,4], 
            2:[1,5], 
            3:[0,4,6],
            4:[1,3,5,7],
            5:[2,4,8],
            6:[3,7],
            7:[6,4,8],
            8:[7,5],
        }

        k_index = state.index(0)

        if direction == "up":
            swap_index = k_index-3
        elif direction == "down":
            swap_index = k_index+3
        elif direction == "left":
            swap_index = k_index-1
        elif direction == "right":
            swap_index = k_index+1
        
        if swap_index < 0 or swap_index > len(state)-1: 
            return None

        if swap_index in index_dir[k_index]:
            pass
        else:
            return None

        swap_data = state[swap_index]
        
        temp[k_index]=swap_data
        temp[swap_index]=0

        return temp
    
    def get_child_node(self,gid):
        result = []

        direction_array = ["up","down","left","right"]

        for direction in direction_array:
            if self.swap_element(self.graph[gid]['state'],direction)!=None:
                child_node = {}
                child_node['depth']=self.graph[gid]['depth']+1
                child_node['state']=self.swap_element(self.graph[gid]['state'],direction)
                child_node['parent']=gid
                child_node['cost']=self.graph[gid]['cost']+1
                result.append(child_node)

        return result
    
    
    def expansion(self,gid):
        if self.graph[gid]['state'] in self.get_path(gid):
            self.fringe.remove(gid)
            self.visited.append(gid)
        else:
            self.fringe.remove(gid)
            self.visited.append(gid)
            
            if self.graph[gid]['state'] == self.goal_state:
                self.finished=True
                self.solution=self.graph[gid]
            else:            
                children=self.get_child_node(gid)            
                for child in children:
                    self.n_node+=1
                    self.graph[self.n_node]=child           
                    self.fringe.append(self.n_node)
    
    def get_dist(self, state): 
        count = None

        if state!=None:
            for i in range(len(state)):
                if state[i] != self.goal_state[i]:
                    if count == None:
                        count = 0
                    count+=1

        return count
    
    def astar(self):

        direction_array = ["up","down","left","right"]

        self.expansion(0)

        while not self.finished:

            f_value = None
            f_index = None

            for i in self.fringe:

                h_min_value = None

                for direction in direction_array:
                    if ( 
                            h_min_value == None or 
                            self.get_dist(self.swap_element(self.graph[i]['state'],direction)) != None and
                            h_min_value > self.get_dist(self.swap_element(self.graph[i]['state'],direction)) 
                        ):
                        h_min_value = self.get_dist(self.swap_element(self.graph[i]['state'],direction)) 

                if (
                        f_value == None or 
                        f_value > self.graph[i]['cost'] + h_min_value
                    ):
                    f_value = self.graph[i]['cost'] + h_min_value
                    f_index = i
                    
            self.expansion(f_index)

    def get_path(self,gid):
        result=[]
        parent=self.graph[gid]['parent']     
        while parent!=None:
            result.append(self.graph[parent]['state'])
            parent=self.graph[parent]['parent']
        return result    
    
    def print_state(self):
        print('fringe:',self.fringe)
        print('visited:',self.visited)

test=agent([6,1,5,0,2,4,7,3,8])
test.astar()