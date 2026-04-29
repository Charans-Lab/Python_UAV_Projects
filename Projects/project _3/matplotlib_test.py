import matplotlib.pyplot as plt

x = [1,2,3]
y = [4,9,6]
z = [1,2,3]
fig, ax = plt.subplots()

for i in z:
    if i == 1:
        ax.scatter(x[i-1],y[i-1], marker='o', c= 'g')
        ax.annotate(i, xy= (x[i-1],y[i-1]))
    elif i == len(z):
        ax.scatter(x[i-1],y[i-1], marker='o', c='r')
        ax.annotate(i, xy= (x[i-1],y[i-1]))
    else:
        ax.scatter(x[i-1],y[i-1], marker='o', c= 'b')
        ax.annotate(i, xy= (x[i-1],y[i-1]))

plt.plot(x,y)
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Mission Plan-Total distance:")
plt.show()











