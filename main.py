
# First we write an elementary code and then we make it an advenced one

# LET'S GET START



#libraries
import random


# First i must fegure out how to make a random game boared
def make_game_board (size_ho,size_ve) :
    numbers=[x for x in range(size_ho* size_ve)] 
    random.shuffle(numbers)
    return numbers


# make goal board
def make_goal_board(size_ho,size_ve):
    goal_board=[x for x in range(size_ho* size_ve)]
    return goal_board


# I need a function to comput every H when i need to
#compute the "h(x)" of every node
def h_Compute(current_board,goal_board,size_ho,size_ve):
    hx=0
    for i in range(size_ho*size_ve):
        if current_board[i] != 0 and current_board[i] != goal_board[i]:
        
            ds = goal_board.index(current_board[i])
            y = (i // size_ve) - (ds // size_ve)
            x = (i % size_ve) - (ds % size_ve)
            hx += abs(y) + abs(x)
    return hx


#this function change the old board to the new one.and change is because of the moving black_space
def replacement(board,past,new):
    data = list(board)
    tmp = data[past]
    data[past] = data[new]
    data[new] = tmp
    return tuple(data)


#first found sides that black space could move
#then found new state for black space
def move_oriented(board,size_ho,size_ve):
    move_nodes = []
    blank = board.index(0)
    
    if blank % size_ve > 0:
        new_child = replacement(board,blank,blank-1)
        move_nodes.append(new_child)
        
    if blank % size_ve + 1 < size_ve:
        new_child = replacement(board,blank,blank+1)
        move_nodes.append(new_child)
        
    if blank - size_ho >= 0:
        new_child = replacement(board,blank,blank-size_ve)
        move_nodes.append(new_child)
        
    if blank + size_ho < len(board):
        new_child = replacement(board,blank,blank+size_ve)
        move_nodes.append(new_child)
        
    return move_nodes


# here we found the goal.so we need the path to get to the goal
def show_path(camefrom,size_ho,size_ve):
    i=1
    for step in camefrom:
        print("{} :".format(i),end='')
        i+=1
        print(step)
        


#A_star search alghorithm for founding new nodes until to the goal
def search(puzzle_b,goal_b,size_ho,size_ve):
    
    #we keep informations about nodes in dictionary which shows beneath
    close_set={}
    open_set={}
    open_set={puzzle_b : None}
    gScore={puzzle_b : 0}
    fScore={puzzle_b : h_Compute(puzzle_b,goal_b,size_ho,size_ve)+ gScore[puzzle_b]}
    number_of_nodes=1
    #for choozen minimume fx
    best_choose=[(gScore[puzzle_b], fScore[puzzle_b])]
    
    while open_set:
        
        #we sorted the chileds with they'r fx score
        best_choose=sorted(best_choose, key=lambda x:x[1])
        print(best_choose[0])
        best_g,best_f= best_choose[0]
        for i in open_set:
            if (gScore[i] ==  best_g) and  (fScore[i] == best_f):
                current_node=i
                break
            
        parent=open_set[current_node]
        
        #if we found the goal so we need path of reaching goal
        #open_set keeps the information about each node and it's parent
        if current_node==goal_b:
            #came_from has goal path
            came_from=[current_node]
    
            while parent is not None:
                came_from.append(parent)
                parent=close_set[parent]
                
            #sort nodes from first to end
            came_from.reverse()
            return came_from
        
        #we dont need to keep this node any more
        #so we remove it from open_set and best_choose.then add to close_set
        del open_set[current_node]
        close_set[current_node]=(parent)
        del best_choose[0]
        
        #gx for each chiled should be this:
        tentetive_gx=gScore[current_node] + 1
        #every edge gsCore=1
        
        del gScore[current_node]
        del fScore[current_node]
        
        #found chileds
        childs=move_oriented(current_node,size_ho,size_ve)
        
        for each_c in childs:
            if each_c in close_set:
                continue
            
            #hx for each chileds
            tentetive_hx=h_Compute(each_c,goal_b,size_ho,size_ve)
            
            #here we check if we added this node to open_set befor and it has a smaller fx ,so we can ignore this new chiled
            if each_c in open_set:
                if fScore[each_c] <= tentetive_gx+tentetive_hx:
                        continue
            
            # each_c is completly new and we dont have it in open_set or close_set
            #so we add new child to open_set
            else:
                open_set[each_c]=current_node
                gScore[each_c]=tentetive_gx
                fScore[each_c]=tentetive_hx + tentetive_gx
                best_choose.append((tentetive_gx, tentetive_gx+tentetive_hx))
                
                number_of_nodes+=1
                print(number_of_nodes)
                print(each_c)
                
    return False
        
        
        
    
if __name__ == '__main__':
    
    print("I need to give me the number of rows and columns.")
    
    size_horizontal=int(input("ROWS:\t"))
    size_vertical=int(input("COLUMNS:\t"))
    #puzzle_board=tuple(make_game_board(size_horizontal,size_vertical))
    puzzle_board=(4,1,2,3,5,0,6,7,8,9,10,11,12,13,14,15)
    goal_board=tuple(make_goal_board(size_horizontal,size_vertical))
    path_to_goal=search(puzzle_board,goal_board,size_horizontal,size_vertical)
    if path_to_goal == False:
        print('we couldent solve the puzzle!')
    else:
        show_path(path_to_goal,size_horizontal,size_vertical)
    
