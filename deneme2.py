import ezdxf
dxf_file = 'Seksek.DXF'

doc = ezdxf.readfile(dxf_file)
msp = doc.modelspace()
#print(msp)
coordinates = []  # Koordinatları depolamak için boş bir dizi

# Iterate over the entities in the modelspace
for entity in msp:
    if entity.dxftype() == 'LINE':  # Sadece çizgi tiplerini kontrol etmek isterseniz
        start = entity.dxf.start
        end = entity.dxf.end
        
        #print(start)
        #print(end)
        coordinates.append(start[0])  # Başlangıç x koordinatını diziye ekle
        coordinates.append(start[1])  # Başlangıç y koordinatını diziye ekle
        coordinates.append(end[0])  # Bitiş x koordinatını diziye ekle
        coordinates.append(end[1])  # Bitiş y koordinatını diziye ekle



# DXF dosyanızın yolunu belirtin


# Koordinatları al
coordinate_array = coordinates
#print(coordinate_array)
# Koordinatları bastır
for i in range(0, len(coordinate_array), 4):
    start_x = coordinate_array[i]
    start_y = coordinate_array[i+1]
    end_x = coordinate_array[i+2]
    end_y = coordinate_array[i+3]
    print(f"Çizgi {i//4+1}: Başlangıç: ({start_x}, {start_y}), Bitiş: ({end_x}, {end_y})")




import ezdxf
import matplotlib.pyplot as plt


# Specify the path to your DXF file
dxf_file = 'Seksek.DXF'
# Specify the path to save the PNG image
save_path = 'dddxfimage.png'

doc = ezdxf.readfile(dxf_file)
msp = doc.modelspace()

# Initialize the bounding box coordinates
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

# Iterate over all entities in the modelspace
for entity in msp:
    if entity.dxftype() == 'LINE':
        start = entity.dxf.start
        end = entity.dxf.end
        min_x = min(min_x, start[0], end[0])
        min_y = min(min_y, start[1], end[1])
        max_x = max(max_x, start[0], end[0])
        max_y = max(max_y, start[1], end[1])

# Create a figure and axis
fig, ax = plt.subplots()

# Iterate over the entities and plot them
for entity in msp:
    if entity.dxftype() == 'LINE':
        start = entity.dxf.start
        end = entity.dxf.end
        ax.plot([start[0], end[0]], [start[1], end[1]], 'k-')

# Set the limits of the plot to match the bounding box
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

# Set the aspect ratio to 'equal' for proper scaling
ax.set_aspect('equal')
plt.show()
# Save the plot as a PNG image
fig.savefig(save_path)



# Save the DXF image as a PNG

