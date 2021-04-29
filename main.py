# LET'S GET START

#libraries
import random
import os

#varieble:
Weight=10

#clear the page
def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
        
        
#choose on of the predifined boards
def predefined_puzzle():
    clear()
    define_puzzle=[([3,1,2,6,4,5,7,0,8], 3), ([1,4,2,0,7,5,3,6,8], 3), \
                   ([3,1,2,6,5,8,7,4,0], 3), ([3,0,2,6,1,5,7,4,8], 3), \
                   ([1,2,3,7,4,5,6,11,8,9,10,0,12,13,14,15], 4), \
                   ([4,1,2,3,8,5,6,7,12,10,11,15,13,9,14,0], 4), \
                   ([1,2,6,3,4,5,7,11,8,13,9,15,12,0,10,14], 4), \
                   ([1,5,2,3,8,4,7,11,12,10,6,0,13,9,14,15], 4), \
                   ([0,4,2,3,8,1,6,7,12,5,10,11,13,9,14,15], 4), \
                   ([5,1,2,3,4,10,6,7,8,9,11,12,13,14,19,15,16,17,18,0,20,21,22,23,24], 5)]
    puzzle=random.choice(define_puzzle)
    return puzzle


# First i must fegure out how to make a random game boared
def make_game_board (size) :
    clear()
    numbers=[x for x in range(size* size)] 
    while 1:
        clear()
        random.shuffle(numbers)
        print("random puzzle is : ")
        print_pretty(numbers,size)
        answer=input("is that good?(remmeber hard puzzle takes a lot time!)(y or n): ")
        if answer.lower() == 'y':
            return numbers


# print our puzzle like a pezzle
def print_pretty(puzzle,size):
    for slash in range(size):
        print("___",end='')
    print("")
    for i in range(size):
        print("|",end='')
        for j in range(size):
            state=(size* i)+ j
            if puzzle[state]<10:
                print(" ",end='')
            print("{}|".format(puzzle[state]),end='')
        print("")
        for slash in range(size):
            print("___",end='')
        print("")
    
    
# make goal board
def make_goal_board(size):
    goal_board=[x for x in range(size*size)]
    return goal_board


# I need a function to comput every H when i need to
#compute the "h(x)" of every node
def h_Compute(current_board,goal_board,size):
    hx=0
    for i in range(size**2):
        if current_board[i] != 0 and current_board[i] != goal_board[i]:
        
            ds = goal_board.index(current_board[i])
            y = (i // size) - (ds // size)
            x = (i % size) - (ds % size)
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
def move_oriented(board,size):
    move_nodes = []
    blank = board.index(0)
    
    if blank % size > 0:
        new_child = replacement(board,blank,blank-1)
        move_nodes.append(new_child)
        
    if blank % size + 1 < size:
        new_child = replacement(board,blank,blank+1)
        move_nodes.append(new_child)
        
    if blank - size >= 0:
        new_child = replacement(board,blank,blank-size)
        move_nodes.append(new_child)
        
    if blank + size < len(board):
        new_child = replacement(board,blank,blank+size)
        move_nodes.append(new_child)
        
    return move_nodes


# here we found the goal.so we need the path to get to the goal
def show_path(camefrom,size):
    i=1
    for step in camefrom:
        print("\n***step {}***\n".format(i))
        print_pretty(step,size)
        i+=1


#A_star search alghorithm for founding new nodes until to the goal
def search(puzzle_b,goal_b,size):
    
    #we keep informations about nodes in dictionary which shows beneath
    close_set={}
    open_set={}
    open_set={puzzle_b : None}
    gScore={puzzle_b : 0}
    fScore={puzzle_b : h_Compute(puzzle_b,goal_b,size)* Weight+ gScore[puzzle_b]}
    number_of_nodes=1
    #for choozen minimume fx
    best_choose=[(gScore[puzzle_b], fScore[puzzle_b])]
    
    while open_set:
        
        #we sorted the chileds with they'r fx score
        best_choose=sorted(best_choose, key=lambda x:x[1])
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
        
        if tentetive_gx >=(size*2)*100:
            continue
        
        #found chileds
        childs=move_oriented(current_node,size)
        
        for each_c in childs:
            if each_c in close_set:
                continue
            
            #hx for each chileds
            tentetive_hx=h_Compute(each_c,goal_b,size)*Weight
            
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
                print("node number:",number_of_nodes)
                print(each_c)
                
    return False
        
        
if __name__ == '__main__':
    clear()

    while 1 :
        clear()
        print("hey Welcom to the N_puzzle game.")
        print("1- TRY RANDOM BOARD.")
        print("2- TRY ONE OF MY PREDIFINED PUZZLES.",end='')
        print("(they are easy to find and you can see the answer fast)")
        print("(random puzzles might takes alot time).")
        answer=input("please choose one: ")
        
        if answer== '1':
            clear()
            print("I need to give me the number of rows and columns.")
            size=int(input("SIZE OF PUZZLE(enter an for n*n puzzle):\t"))
            puzzle_board=tuple(make_game_board(size))
            goal_board=tuple(make_goal_board(size))
            break
                
        elif answer== '2':
            choose=predefined_puzzle()
            puzzle_board, size=choose
            goal_board=tuple(make_goal_board(size))
            print("the puzzle boared is: ")
            print_pretty(puzzle_board,size)
            break
            
        else:
            continue
    

    path_to_goal=search(tuple(puzzle_board),goal_board,size)
    if path_to_goal == False:
        print('we couldent solve the puzzle!')
    else:
        show_path(path_to_goal,size)
    
