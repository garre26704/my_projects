import bpy  

current_obj = bpy.context.active_object  
verts_local = [v.co for v in current_obj.data.vertices.values()]
verts_world = [current_obj.matrix_world @ v_local for v_local in verts_local]

print("="*40) # printing marker
file_punti = open("C:/Users/Gabri/Documents/3d_renderer_python/modello_punti.txt", "w")
file_connessioni=open("C:/Users/Gabri/Documents/3d_renderer_python/modello_connessioni.txt", "w")

for i, vert in enumerate(verts_world):
    file_punti.write(("({v[0]}, {v[1]}, {v[2]}) \n".format(i=i, v=vert)))

for i, face in enumerate(current_obj.data.polygons):
    verts_indices = face.vertices[:]
    file_connessioni.write(("{v_i} \n".format(i=i, v_i=verts_indices)))          
    
file_punti.close()
file_connessioni.close()
