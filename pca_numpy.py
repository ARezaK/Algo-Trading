import numpy as np
np.random.seed(1)

mu_vec1 = np.array([0,0,0])
cov_mat1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class1_sample = np.random.multivariate_normal(mu_vec1,cov_mat1, 20).T
print class1_sample

assert class1_sample.shape == (3,20), "The matrix has not the dimensions 3x20"

mu_vec2 = np.array([1,1,1])
cov_mat2 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class2_sample = np.random.multivariate_normal(mu_vec2,cov_mat2, 20).T
print class2_sample

assert class2_sample.shape == (3,20), "The matrix has not the dimensions 3x20"

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(class1_sample[0,:], class1_sample[1,:],
        class1_sample[2,:],'o', markersize=8, color='blue', alpha=0.5, label='class1')
ax.plot(class2_sample[0,:], class2_sample[1,:],
        class2_sample[2,:],'^', markersize=8, color='red', alpha=0.5, label='class2')
plt.title("Samples")
plt.show()

#b/c we dont need class labels lets mrege the 2 samples
all_samples = np.concatenate((class1_sample, class2_sample), axis=1)

#computing the mean vector
mean_x = np.mean(all_samples[0,:])
mean_y = np.mean(all_samples[1,:])
mean_z = np.mean(all_samples[2,:])

mean_vector = np.array([[mean_x,], [mean_y], [mean_z]])
print "mean vector: \n", mean_vector

#calculate covariance matrix
cov_mat = np.cov([all_samples[0,:],all_samples[1,:],all_samples[2,:]])

print "covariance matrix : \n", cov_mat

#calcluate eigenvectors and eignevalues
eig_values_cov, eig_vectors_cov = np.linalg.eig(cov_mat)


#plot eigenvectors centered at the sample mean
from matplotlib.patches import FancyArrowPatch

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')

ax.plot(all_samples[0,:], all_samples[1,:],\
    all_samples[2,:], 'o', markersize=8, color='green', alpha=0.2)
ax.plot([mean_x], [mean_y], [mean_z], 'o', \
    markersize=10, color='red', alpha=0.5)
for v in eig_vectors_cov.T:
    a = Arrow3D([mean_x, v[0]], [mean_y, v[1]],\
        [mean_z, v[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.add_artist(a)
ax.set_xlabel('x_values')
ax.set_ylabel('y_values')
ax.set_zlabel('z_values')

plt.title('Eigenvectors')

plt.show()

#sorting the eignevecots by decreasing eignevalues
#to remove the ones that dont hold releveant information

#make a list of (eigenvalue, eigenvector) tupels
eig_pairs = [(np.abs(eig_values_cov[i]), eig_vectors_cov[:,i]) for i in range(len(eig_values_cov))]

#sort from high to low
eig_pairs.sort()
eig_pairs.reverse()

#visually confirm by lowwing at eignevalues
print "eigenvalues"
for i in eig_pairs:
    print(i[0])

#now lets create a new matrix with only the two highest eigenvalues
#basically matrix w is the collection of your princial components
matrix_w = np.hstack((eig_pairs[0][1].reshape(3,1), eig_pairs[1][1].reshape(3,1)))
print "Matrix W :\n", matrix_w


#transofrming the smaples onto the new subspace
#use the new W matrix to transofrm our smaples onto the new subspace
#y = w^T * x
transformed = matrix_w.T.dot(all_samples)

plt.plot(transformed[0,0:20], transformed[1,0:20],\
     'o', markersize=7, color='blue', alpha=0.5, label='class1')
plt.plot(transformed[0,20:40], transformed[1,20:40],
     '^', markersize=7, color='red', alpha=0.5, label='class2')
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.xlabel('x_values')
plt.ylabel('y_values')
plt.legend()
plt.title('Transformed samples with class labels')


plt.show()


#now lets do the samething using matlab pca
from matplotlib.mlab import PCA as mlPCA

mlab_pca = mlPCA(all_samples.T)
print('PC axes in terms of the measurement axes'\
        ' scaled by the standard deviations:\n',\
          mlab_pca.Wt)

plt.plot(mlab_pca.Y[0:20,0],mlab_pca.Y[0:20,1], 'o', markersize=7,\
        color='blue', alpha=0.5, label='class1')
plt.plot(mlab_pca.Y[20:40,0], mlab_pca.Y[20:40,1], '^', markersize=7,\
        color='red', alpha=0.5, label='class2')

plt.xlabel('x_values')
plt.ylabel('y_values')
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.legend()
plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')

plt.show()

#if you look at these graphs you'll see that they do not look identical. This is b/c the pca function from matlab scales teh variables to
#unit variance prior to calculating the covariance matrices. This will/cloud eventually lead to different variances along the axes

#You should only be scaling if one variable of the data is measured in inches and the other was say measured in newtons
#for this example we assumed the data was in the same units so we skpped the step of scaling
