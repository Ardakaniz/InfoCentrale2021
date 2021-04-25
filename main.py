import raytracer
import data
import time
from PIL import Image

def write_image():
	im = Image.new("RGB", (data.PX_COUNT, data.PX_COUNT))
	im_px = im.load()
	px = raytracer.lancer(data.viewer, data.background_color)

	for j in range(data.PX_COUNT):
		for i in range(data.PX_COUNT):
			R, G, B = px[i, j, :]
			if R > 1: R = 1
			if G > 1: G = 1
			if B > 1: B = 1
			im_px[i, j] = (int(R*255), int(G*255), int(B*255))

	im.save("output.png")

if __name__ == "__main__":
	start = time.perf_counter()
	write_image()
	end = time.perf_counter()
	print(f"Generated in {end - start:0.4f}s.")