import numba as nb
import math
import numpy as np
import GameRex as GR

class modello:
    def __init__(self, poin, tri, pos, size, vel, an=[0,0,0]):
        self.poin = poin
        self.tri = tri
        self.pos = pos
        self.size = size
        self.vel = vel
        self.an = an
        self.index = 0
        self.luce = np.array([0, 0, -1, 0])
        self.colori = []

    def scansiona_dati(self, P_file, lista):
        with open(P_file, "r") as f:
            for d in f:
                n = d.replace("(", "")
                c = n.replace(") \n", "")
                data = c.split(",", 33)
                for elemento in data:
                    if P_file == "C:/Users/Gabri/Documents/3d_renderer_python/modello_punti.txt":
                        f_elemento = float(elemento)
                        data[data.index(elemento)] = f_elemento * 100
                    else:
                        i_elemento = int(elemento)
                        data[data.index(elemento)] = i_elemento
                if P_file == "C:/Users/Gabri/Documents/3d_renderer_python/modello_punti.txt":
                    data.append(1)
                lista.append(data)

    def sort_data(self):
        z_index=[]
        for punti in self.poin:
            z_index.append(punti[2])
        z_index=np.sort(z_index,0)
        #print(z_index)
        for z in range(len(z_index)):
            self.poin[z][2]=z_index[z]
        return self.poin

    
    def genera_vettori(self):
        self.coppia_vettori = []
        for triangolo in self.tri:
            v1 = np.subtract(self.poin[triangolo[1]], self.poin[triangolo[0]])
            v2 = np.subtract(self.poin[triangolo[2]], self.poin[triangolo[0]])
            self.coppia_vettori.append([v1, v2])

    def calculate_cross_prod(self):
        self.vettori_normali = []
        for coppia in self.coppia_vettori:
            nx = (coppia[0][1] * coppia[1][2]) - (coppia[0][2] * coppia[1][1])
            ny = (coppia[0][2] * coppia[1][0]) - (coppia[0][0] * coppia[1][2])
            nz = (coppia[0][0] * coppia[1][1]) - (coppia[0][1] * coppia[1][0])
            normal_v = np.array([nx, ny, nz, 0])
            if np.sum(normal_v) != 0:
                n_normal = normal_v / np.linalg.norm(normal_v)
            else:
                n_normal = np.array([0, 0, 0, 0])
            self.vettori_normali.append(n_normal)
        return self.vettori_normali

    #@nb.jit
    def dot(self, m):
        for i in range(len(self.poin)):
            if len(self.poin[i]) == 4:
                nuovo_punto = np.dot(m, self.poin[i])
                self.poin[i] = nuovo_punto
        return self.poin

    def rotate_model(self):
        rot_mat_x = [[1, 0, 0, 0],
                     [0, math.cos(math.radians(self.an[0])), math.sin(math.radians(self.an[0])), 0],
                     [0, -math.sin(math.radians(self.an[0])), math.cos(math.radians(self.an[0])), 0],
                     [0,0,0,0]]
        
        rot_mat_y=[[math.cos(math.radians(self.an[1])),0,math.sin(math.radians(self.an[1])),0],
                   [0,1,0,0],
                   [-math.sin(math.radians(self.an[1])),0,math.cos(math.radians(self.an[1])),0],
                   [0,0,0,0]]
        
        rot_mat_z=[[math.cos(math.radians(self.an[2])),math.sin(math.radians(self.an[2])),0,0],
                   [-math.sin(math.radians(self.an[2])),math.cos(math.radians(self.an[2])),0,0],
                   [0,0,1,0],
                   [0,0,0,0]]
        
        self.an[0]+=0.5
        self.an[1]+=0.5
        self.an[2]+=0.5
        
        self.poin=self.dot(rot_mat_x)
        self.poin=self.dot(rot_mat_y)
        self.poin=self.dot(rot_mat_z)
        
    def scale_model(self):
        scal_mat=[[self.size[0],0,0,0],
                  [0,self.size[1],0,0],
                  [0,0,self.size[2],0],
                  [0,0,0,0]]
        self.poin=self.dot(scal_mat)

    def transform_model(self):
        transform_mat=[[1,0,0,self.pos[0]],
                       [0,1,0,self.pos[1]],
                       [0,0,1,self.pos[2]],
                       [0,0,0,0]]
        self.poin=self.dot(transform_mat)

    
    def illumina(self):
        self.luce=self.luce/np.linalg.norm(self.luce)
        self.colori=[]
        for triangolo in range(len(self.tri)):
            if (((self.poin[self.tri[triangolo][0]][0]*self.poin[self.tri[triangolo][1]][1])-(self.poin[self.tri[triangolo][0]][1]*self.poin[self.tri[triangolo][1]][0]))+
                ((self.poin[self.tri[triangolo][1]][0]*self.poin[self.tri[triangolo][2]][1])-(self.poin[self.tri[triangolo][1]][1]*self.poin[self.tri[triangolo][2]][0]))+
                ((self.poin[self.tri[triangolo][2]][0]*self.poin[self.tri[triangolo][0]][1])-(self.poin[self.tri[triangolo][2]][1]*self.poin[self.tri[triangolo][0]][0])))<0:
                dot=np.dot(self.vettori_normali[triangolo],self.luce)
                self.colori.append((abs(dot*255),abs(dot*255),abs(dot*255))) 
        return self.colori
   
            
    
    def genera_modello(self):
        m=[]
        m_texture=[]
        for t in range(len(self.tri)):
           
            if (((self.poin[self.tri[t][0]][0]*self.poin[self.tri[t][1]][1])-(self.poin[self.tri[t][0]][1]*self.poin[self.tri[t][1]][0]))+
                ((self.poin[self.tri[t][1]][0]*self.poin[self.tri[t][2]][1])-(self.poin[self.tri[t][1]][1]*self.poin[self.tri[t][2]][0]))+
                ((self.poin[self.tri[t][2]][0]*self.poin[self.tri[t][0]][1])-(self.poin[self.tri[t][2]][1]*self.poin[self.tri[t][0]][0])))<0:#culling
                
                m.append([self.poin[self.tri[t][0]],self.poin[self.tri[t][1]]])
                m.append([self.poin[self.tri[t][1]],self.poin[self.tri[t][2]]])
                m.append([self.poin[self.tri[t][2]],self.poin[self.tri[t][0]]])
                m_texture.append([self.poin[self.tri[t][0]],self.poin[self.tri[t][1]],self.poin[self.tri[t][2]]])
                
        return m,m_texture

    
    def proietta(self,w,h):
        aspect_ratio=h/w
        FOV=60
        z0=(w/2)/math.tan(np.deg2rad(FOV))
        
        for p in range(len(self.poin)):
            if len(self.poin[p])==4 :
                nuovo_punto=[((z0/(z0+self.poin[p][2]))*self.poin[p][0])*aspect_ratio,((z0/(z0+self.poin[p][2]))*self.poin[p][1])*aspect_ratio]
                self.poin[p]=nuovo_punto
                   
        return self.poin
    
    def aggiorna_modello(self):
        
        self.poin=[]
        self.tri=[]
        self.scansiona_dati("C:/Users/Gabri/Documents/3d_renderer_python/modello_punti.txt",self.poin)
        self.scansiona_dati("C:/Users/Gabri/Documents/3d_renderer_python/modello_connessioni.txt",self.tri)
        self.transform_model()
        self.rotate_model()
        self.scale_model()
        self.genera_vettori()
        self.vettori_normali=self.calculate_cross_prod()
        self.poin=self.sort_data()
        self.poin=self.proietta(1000,1000)
        self.colori=self.illumina()
        self.modello,self.modello_texture=self.genera_modello()
        
        
        
        
               
triangoli=[]
points=[]        
s=[1,1,1]#size
p=[0,0,0]#position
v=[1,1,1]#velocity
an=[-90,0,0]#an
m1=modello(points,triangoli,p,s,v,an)     






    
class scena(): 
      
    def __init__(self,w,h):
        
        self.Main=GR.Main("3d renderer",w,h)
        self.origine=[w/2,h/2]

    def draw_segment(self,modello):
        for line in modello:
            self.Main.draw_line("red",line[0][0]+self.origine[0],line[0][1]+self.origine[1],line[1][0]+self.origine[0],line[1][1]+self.origine[1])
            
    def draw_poli(self,modello_colori,modello_texture):   
        for L in range(len(modello_texture)):
            
            self.Main.draw_polygon(modello_colori[L],modello_texture[L][2][0]+self.origine[0],modello_texture[L][2][1]+self.origine[1],modello_texture[L][1][0]+self.origine[0],modello_texture[L][1][1]+self.origine[1],modello_texture[L][0][0]+self.origine[0],modello_texture[L][0][1]+self.origine[1])
          
    def aggiorna(self):
        while True:
            m1.aggiorna_modello()
            self.draw_poli(m1.colori,m1.modello_texture)
            #self.draw_segment(m1.modello)
            self.Main.run()



s=scena(1000,1000)
s.aggiorna()  
