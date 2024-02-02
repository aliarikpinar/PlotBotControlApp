#
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
#import wx
import glob
import re


default_img_format = '.png'
default_img_res = 300
img_format=default_img_format
img_res=default_img_res
doc = ezdxf.readfile(r"sqaure.png")
msp = doc.modelspace()
# Recommended: audit & repair DXF document before rendering
auditor = doc.audit()
# The auditor.errors attribute stores severe errors,
# which *may* raise exceptions when rendering.
if len(auditor.errors) != 0:
    raise exception("The DXF document is damaged and can't be converted!")
else :
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    ctx.set_current_layout(msp)
    ctx.current_layout.set_colors(bg='#FFFFFF')
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(msp, finalize=True)

    img_name = re.findall("(\S+)\.",name)  # select the image name that is the same as the dxf file name
    first_param = ''.join(img_name) + img_format  #concatenate list and string
    fig.savefig(first_param, dpi=img_res)




# import cv2
# import numpy as np
# from svgpathtools import svg2paths, Line
# import svgpathtools
# import webbrowser
# import tempfile
# import os
# import svgwrite
# import time
# image = cv2.imread(r"sqaure.png" )
# # img = imutils.resize(img, width=512)
"""
cv2.imshow('image' , img)

# Convert the image to grayscale

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150)

# Apply Hough Line Transform
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=10, minLineLength=10, maxLineGap=3)

# Draw the lines on the img
line_img = img.copy()


grouped_lines = []

# Thresholds for proximity and parallelism
proximity_threshold = 10  # Adjust this value as needed
parallelism_threshold = np.pi / 18  # Adjust this value as needed

# Iterate over each line
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]

        # Draw the line on the image
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate the angle of the line
        angle = np.arctan2(y2 - y1, x2 - x1)

        # Find lines that are close and parallel
        merged = False
        for idx, existing_line in enumerate(grouped_lines):
            # Calculate the angle difference
            angle_diff = np.abs(existing_line['angle'] - angle)

            # Calculate the distance between line endpoints
            dist1 = np.linalg.norm(existing_line['endpoints'][0] - np.array([x1, y1]))
            dist2 = np.linalg.norm(existing_line['endpoints'][1] - np.array([x2, y2]))

            # Check if the lines are close and parallel
            if angle_diff < parallelism_threshold and (dist1 < proximity_threshold or dist2 < proximity_threshold):
                # Merge the lines by updating the endpoints
                existing_line['endpoints'][0] = np.array([min(existing_line['endpoints'][0][0], x1),
                                                          min(existing_line['endpoints'][0][1], y1)])
                existing_line['endpoints'][1] = np.array([max(existing_line['endpoints'][1][0], x2),
                                                          max(existing_line['endpoints'][1][1], y2)])
                merged = True
                break

        # If the line was not merged with any existing line, add it as a new grouped line
        if not merged:
            grouped_lines.append({'endpoints': [np.array([x1, y1]), np.array([x2, y2])], 'angle': angle})

# Draw the grouped lines on the image
for line in grouped_lines:
    pt1 = tuple(map(int, line['endpoints'][0]))
    pt2 = tuple(map(int, line['endpoints'][1]))
    cv2.line(line_img, pt1, pt2, (0, 0, 255), 2)

# Display the image with lines
cv2.imshow('Lines', line_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""


# # Convert the image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply Canny edge detection
# edges = cv2.Canny(gray,200,200)

# # Apply Hough Line Transform
# lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=30, minLineLength=30, maxLineGap=1)
# # Create an SVG drawing
# dwg = svgwrite.Drawing()

# # Iterate over each line
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]

#         # Smooth the line using moving average or spline interpolation
#         smoothed_line = np.linspace((x1, y1), (x2, y2), num=50)  # Example: using linear interpolation

#         # Add the smoothed line to the SVG drawing
#         dwg.add(dwg.line(start=(smoothed_line[0][0], smoothed_line[0][1]),
#                          end=(smoothed_line[-1][0], smoothed_line[-1][1]),
#                          stroke='black',
#                          stroke_width=2))

# # Save the SVG content to a temporary file
# temp_file = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
# dwg.saveas(temp_file.name)
# temp_file.close()

# # Wait for 1 second before opening the SVG file
# time.sleep(1)

# # Open the SVG file in the default web browser
# webbrowser.open('file://' + os.path.realpath(temp_file.name))

# time.sleep(20)
