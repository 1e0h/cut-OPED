import subprocess

print("Enter File")
movie: str = input(">> ")
output = subprocess.run(["ffmpeg", "-i", movie, "-af", "silencedetect=d=0.4", "-f", "null", "-"],
						stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(output)
text = str(output)
lines = text.split("\\n")
start_list = []
end_list = []
for line in lines:
	if "silencedetect" in line:
		times = line.split(" ")
		for i in range(len(times)):
			if "silence_start" in times[i]:
				start_list.append(times[i + 1][:-2])
			if "silence_end" in times[i]:
				end_list.append(times[i + 1])
try:
	for i in range(len(start_list)):
		if float(start_list[i]) > 1300:
			ED_end = float(start_list[i])
			if float(start_list[i + 2]) - float(start_list[i]) > 30:
				ED_end = float(start_list[i + 2])
			else:
				break
		if float(start_list[i]) > 10:
			OP_end = float(start_list[i])
except:
	print("error")
print(OP_end)
print(ED_end)
index = movie.rfind(".")
OP_pass = movie[:index] + "_OP.mp4"
ED_pass = movie[:index] + "_ED.mp4"
OP_start = OP_end - 89
ED_start = ED_end - 89
output = subprocess.run(["ffmpeg", "-ss", str(OP_start), "-i", movie, "-t", str(89.5), OP_pass], stdout=subprocess.PIPE,
						stderr=subprocess.PIPE)
print(output)
output = subprocess.run(["ffmpeg", "-ss", str(ED_start), "-i", movie, "-t", str(89.5), ED_pass], stdout=subprocess.PIPE,
						stderr=subprocess.PIPE)
print(output)
