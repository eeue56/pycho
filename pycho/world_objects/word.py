from __future__ import division

from pycho.world_objects import WorldObject
from pycho.world.navigation import DIRECTIONS

from pycho.gl.color import COLORS

try:
    xrange(1)
except NameError:
    xrange = range

class Word(WorldObject):
    def __init__(self, 
        x, 
        y, 
        word, 
        color=COLORS['grey'], 
        facing=DIRECTIONS['up'], 
        speed=0,
        *args,
        **kwargs):
        WorldObject.__init__(self, x, y, color, facing, damagable=False, moveable=False, *args, **kwargs)
        self.word = word

    def tick(self, world):
        pass

    def take_damage(self, damage, world):
        pass

    def populate(self, x, y, list):
        def func(i, j):
            list.append((x + i, y + j, self.color))

        return func

    def populate_a(self, x, y):

        #  #####
        #  #   #
        #  ##### 
        #  #   #
        #->#   #

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            if i in (0, 4):
                for j in xrange(5):
                    populate(i, j)

            populate(i, 4)
            populate(i, 2)

        return populated

    def populate_b(self, x, y):

        #  #####   
        #  #  ##
        #  ###
        #  #  ##  
        #->#####

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            populate(i, 0)
            populate(i, 4)

            if i < 3:
                populate(i, 2)

            if i in (0, 3, 4):
                populate(i, 1)
                populate(i, 3)

        return populated

    def populate_c(self, x, y):

        #    ###  
        #   # 
        #  #
        #   #  
        #->  ###

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            if i > 1:
                populate(i, 0)
                populate(i, 4)
            elif i < 1:
                populate(i, 2)
            else:
                populate(i, 3)
                populate(i, 1)

        return populated

    def populate_d(self, x, y):

        #  ###  
        #  #  #
        #  #   #
        #  #  #
        #->###

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            if i < 1:
                for j in xrange(5):
                    populate(i, j)
            elif i < 3:
                populate(i, 0)
                populate(i, 4)
            elif i < 4:
                populate(i, 1)
                populate(i, 3)
            else:
                populate(i - 1, 2)

        return populated

    def populate_e(self, x, y):

        #  #####
        #  #
        #  ####   
        #  #  
        #->#####

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            if i < 1:
                for j in xrange(5):
                    populate(i, j)
            
            populate(i, 0)
            populate(i, 4)
            
            if i < 4:
                populate(i, 2)

        return populated

    def populate_f(self, x, y):

        #  #####
        #  #
        #  ####   
        #  #  
        #->#

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            if i < 1:
                for j in xrange(5):
                    populate(i, j)

            populate(i, 4)
            
            if i < 4:
                populate(i, 2)

        return populated

    def populate_g(self, x, y):

        #  #####
        #  #  
        #  # ### 
        #  #   #
        #->#####

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            if i < 1:
                for j in xrange(5):
                    populate(i, j)

            populate(i, 0)
            populate(i, 4)
            
            if i > 1:
                populate(i, 2)

            if i == 4:
                populate(i, 1)

        return populated

    def populate_h(self, x, y):

        #  #   #
        #  #   #
        #  ##### 
        #  #   #
        #->#   #

        populated = []
        populate = self.populate(x, y, populated)
        middle_x = 2
        middle_y = 2

        for i in xrange(5):
            if i in (0, 4):
                for j in xrange(5):
                    populate(i, j)

            populate(i, 2)

        return populated

    def populate_i(self, x, y):

        #  #####
        #    #  
        #    # 
        #    #  
        #->#####

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 2:
                for j in xrange(5):
                    populate(i, j)

            populate(i, 0)
            populate(i, 4)

        return populated

    def populate_j(self, x, y):

        #  #####
        #     #  
        #     # 
        #     #  
        #->###

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 3:
                for j in xrange(5):
                    populate(i, j)

            if i < 3:
                populate(i, 0)
            populate(i, 4)

        return populated

    def populate_k(self, x, y):

        #  #  #
        #  # # 
        #  ## 
        #  # #   
        #->#  #

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 0:
                for j in xrange(5):
                    populate(i, j)
            elif i == 1:
                populate(i, 2)
            elif i == 2:
                populate(i, 1)
                populate(i, 3)
            elif i == 3:
                populate(i, 0)
                populate(i, 4)


        return populated

    def populate_l(self, x, y):

        #  #
        #  # 
        #  #
        #  #    
        #->#####

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 0:
                for j in xrange(5):
                    populate(i, j)
            populate(i, 0)
               


        return populated

    def populate_n(self, x, y):

        #  #   #
        #  ##  #
        #  # # #
        #  #  ## 
        #->#   #

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 0 or i == 4:
                for j in xrange(5):
                    populate(i, j)
            elif i == 1:
                populate(i, 3)
            elif i == 2:
                populate(i, 2)
            elif i == 3:
                populate(i, 1)              


        return populated

    def populate_o(self, x, y):

        #   ### 
        #  #   #
        #  #   #
        #  #   # 
        #-> ###

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 0 or i == 4:
                for j in xrange(1, 4):
                    populate(i, j)
            else:
                populate(i, 0)
                populate(i, 4)          


        return populated

    def populate_p(self, x, y):

        #  #### 
        #  #   #
        #  ####
        #  #    
        #->#

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 0:
                for j in xrange(5):
                    populate(i, j)
            elif i < 4:
                populate(i, 2)
                populate(i, 4)
            else:
                populate(i, 3)          


        return populated

    def populate_q(self, x, y):

        #   ####
        #  #   #
        #   ####
        #      #    
        #->    #

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 0:
                populate(i, 3)
            elif i == 4:
                for j in xrange(5):
                    populate(i, j)
            elif i < 4:
                populate(i, 2)
                populate(i, 4)      


        return populated

    def populate_r(self, x, y):

        #  ####
        #  #   #
        #  ####
        #  #  #      
        #->#   #

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            if i == 0:
                for j in xrange(5):
                    populate(i, j)
            elif i == 4:
                populate(i, 3)
                populate(i, 0)
            else:
                populate(i, 2)
                populate(i, 4)   

        populate(3, 1)

        return populated

    def populate_s(self, x, y):

        #  #####
        #  ##   
        #   ###
        #     ##      
        #->#####   

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            populate(i, 4)
            populate(i, 0)

            if i < 2:
                populate(i, 3)

            if i in (1, 2, 3):
                populate(i, 2)

            if i > 2:
                populate(i, 1)


        return populated

    def populate_t(self, x, y):

        #  #####
        #    #   
        #    #
        #    #      
        #->  #   

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            if i == 2:
                for j in xrange(5):
                    populate(i, j)
            else:
                populate(i, 4)


        return populated

    def populate_u(self, x, y):

        #  #    #
        #  #    #   
        #  #    #
        #  #    #      
        #-> ####   

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            if i == 0 or i == 4:
                for j in xrange(1, 5):
                    populate(i, j)
            else:
                populate(i, 0)


        return populated

    def populate_v(self, x, y):

        #  #   #
        #  #   #   
        #  #   #
        #   # #      
        #->  #   

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            if i == 0 or i == 4:
                for j in xrange(2, 5):
                    populate(i, j)
            elif i in (1, 3):
                populate(i, 1)
            else:
                populate(i, 0)


        return populated

    def populate_x(self, x, y):

        #  #    #
        #   #  #   
        #    #
        #   # #      
        #->#   #  

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            if i in (0, 4):
                populate(i, 0)
                populate(i, 4)
            elif i in (1, 3):
                populate(i, 1)
                populate(i, 3)
            else:
                populate(i, 2)


        return populated

    def populate_y(self, x, y):

        #  #    #
        #   #  #   
        #    #
        #    #       
        #->  #   

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            if i in (0, 4):
                populate(i, 4)
            elif i in (1, 3):
                populate(i, 3)
            else:
                for j in xrange(3):
                    populate(i, j)


        return populated

    def populate_z(self, x, y):

        #  #####    
        #     #    
        #    #
        #   #       
        #->#####   

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            populate(i, 0)
            populate(i, 4)

            populate(i, i)

        return populated

    def populate_m(self, x, y):

        #   # #
        #  # # #  
        #  # # #
        #  # # #     
        #->#   #   

        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            if i in (0, 4):
                for j in xrange(4):
                    populate(i, j)
            elif i == 2:
                for j in xrange(1, 4):
                    populate(i, j)
            else:
                populate(i, 4)
            

        return populated
        
    def populate_w(self, x, y):

        #  # # #  
        #  # # #
        #  # # #     
        #  ## ##   
        #->#   #
        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            
            if i in (0, 4):
                for j in xrange(5):
                    populate(i, j)
            elif i == 2:
                for j in xrange(2, 5):
                    populate(i, j)
            else:
                populate(i, 1)
            

        return populated

    def populate_1(self, x, y):

        #   ##   
        #  # # 
        #    #      
        #    #   
        #->#####
        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            populate(i, 0)

            if i == 2:
                for j in xrange(1, 5):
                    populate(i, j)

        populate(0, 3)
        populate(1, 4)
            
        return populated

    def populate_2(self, x, y):

        #   ##   
        #  #  #
        #     #      
        #    #   
        #->#####
        populated = []
        populate = self.populate(x, y, populated)

        for i in xrange(5):
            populate(i, 0)

            if i == 2:
                for j in xrange(1, 3):
                    populate(i, j)
                populate(i, 4)

            if i == 3:
                for j in xrange(2, 4):
                    populate(i, j)

        populate(0, 3)
        populate(1, 4)
            
        return populated

    def populate_3(self, x, y):
        #   ##   
        #  #  #
        #    ##      
        #  #  #  
        #-> ##
        populated = []
        populate = self.populate(x, y, populated)

        populate(0, 1)
        populate(0, 3)
        
        populate(1, 0)
        populate(1, 4)
        
        populate(2, 0)
        populate(2, 4)

        populate(3, 0)
        populate(3, 2)
        populate(3, 4)

        populate(4, 1)
        populate(4, 2)
        populate(4, 3)
        
        return populated

    def populate_4(self, x, y):
        #  #  #   
        #  #  #  
        #  #####      
        #     #  
        #->   #
        populated = []
        populate = self.populate(x, y, populated)

        populate(0, 3)
        populate(0, 4)
        
        populate(2, 0)
        populate(2, 1)
        populate(2, 3)
        populate(2, 4)
        
        for i in xrange(5):
            populate(i, 2)
        
        return populated

    def populate_5(self, x, y):
        #  #####   
        #  #  
        #  ####      
        #      #  
        #->####
        populated = []
        populate = self.populate(x, y, populated)
        
        for i in xrange(5):

            if i < 4:
                populate(i, 2)
                populate(i, 0)

            populate(i, 4)

        populate(0, 3)
        populate(4, 1)
        
        return populated

    def populate_6(self, x, y):
        #    ###   
        #   #  
        #   ###      
        #  #   #  
        #-> ###
        populated = []
        populate = self.populate(x, y, populated)
        
        for i in xrange(1, 4):
            populate(i, 0)
            populate(i, 2)
            populate(i + 1, 4)
            
        populate(0, 1)
        populate(4, 1)
        populate(1, 3)
        
        return populated

    def populate_7(self, x, y):
        #  #####   
        #     #
        #   ###      
        #   #   
        #->#

        populated = []
        populate = self.populate(x, y, populated)
        
        for i in xrange(5):
            populate(i, 4)

        populate(0, 0)
        
        populate(1, 1)
        populate(1, 2)
        populate(2, 2)
        populate(3, 2)

        populate(3, 3)
        
        
        return populated

    def populate_8(self, x, y):
        #   ###   
        #  #   #
        #   ###      
        #  #   #
        #-> ###

        populated = []
        populate = self.populate(x, y, populated)
        
        for j in xrange(5):
            if j in (1, 3):
                populate(0, j)
                populate(4, j)
            else:
                for i in xrange(1, 4):
                    populate(i, j)

        return populated

    def populate_9(self, x, y):
        #  #####   
        #  #   #
        #  #####      
        #      #
        #-> ####

        populated = []
        populate = self.populate(x, y, populated)
        
        for j in xrange(5):
            if j == 1:
                populate(4, j)
            elif j == 3:
                populate(0, j)
                populate(4, j)
            elif j == 0:
                for i in xrange(1, 5):
                    populate(i, j)
            else:
                for i in xrange(5):
                    populate(i, j)

        return populated


    #'abcdefghijklmnopqrstuvwxyz

    def _get_populate_method(self, letter):
        try:
            return self.__getattribute__('populate_{letter}'.format(letter=letter))
        except:
            return lambda *a, **kw: []

    def populated_at(self, x, y):

        old_x = x

        populated = []
        for letter in self.word.lower():
            if letter == '\n':
                y -= 7
                x = old_x
            elif letter == ' ':
                x += 5
            else:
                populated.extend(self._get_populate_method(letter)(x, y))
                x += 7


        return populated
