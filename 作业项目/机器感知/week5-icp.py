import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors


def best_fit_transform(A, B):
    '''
    Calculates the least-squares best-fit transform that maps corresponding points A to B in m spatial dimensions
    Input:
      A: Nxm numpy array of corresponding points
      B: Nxm numpy array of corresponding points
    Returns:
      T: (m+1)x(m+1) homogeneous transformation matrix that maps A on to B
      R: mxm rotation matrix
      t: mx1 translation vector
    '''

    assert A.shape == B.shape

    # get number of dimensions
    m = A.shape[1]

    # translate points to their centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - centroid_A
    BB = B - centroid_B

    # rotation matrix
    H = np.dot(AA.T, BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
       Vt[m-1,:] *= -1
       R = np.dot(Vt.T, U.T)

    # translation
    t = centroid_B.T - np.dot(R,centroid_A.T)

    # homogeneous transformation
    T = np.identity(m+1)
    T[:m, :m] = R
    T[:m, m] = t

    return T, R, t


def nearest_neighbor(src, dst):
    '''
    Find the nearest (Euclidean) neighbor in dst for each point in src
    Input:
        src: Nxm array of points
        dst: Nxm array of points
    Output:
        distances: Euclidean distances of the nearest neighbor
        indices: dst indices of the nearest neighbor
    '''

    assert src.shape == dst.shape

    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(dst)
    distances, indices = neigh.kneighbors(src, return_distance=True)
    return distances.ravel(), indices.ravel()


def icp(A, B, init_pose=None, max_iterations=20, tolerance=0.001):
    '''
    The Iterative Closest Point method: finds best-fit transform that maps points A on to points B
    Input:
        A: Nxm numpy array of source mD points
        B: Nxm numpy array of destination mD point
        init_pose: (m+1)x(m+1) homogeneous transformation
        max_iterations: exit algorithm after max_iterations
        tolerance: convergence criteria
    Output:
        T: final homogeneous transformation that maps A on to B
        distances: Euclidean distances (errors) of the nearest neighbor
        i: number of iterations to converge
    '''

    assert A.shape == B.shape

    # get number of dimensions
    m = A.shape[1]

    # make points homogeneous, copy them to maintain the originals
    src = np.ones((m+1,A.shape[0]))
    dst = np.ones((m+1,B.shape[0]))
    src[:m,:] = np.copy(A.T)
    dst[:m,:] = np.copy(B.T)

    # apply the initial pose estimation
    if init_pose is not None:
        src = np.dot(init_pose, src)

    prev_error = 0

    for i in range(max_iterations):
        # find the nearest neighbors between the current source and destination points
        distances, indices = nearest_neighbor(src[:m,:].T, dst[:m,:].T)

        # compute the transformation between the current source and nearest destination points
        T,_,_ = best_fit_transform(src[:m,:].T, dst[:m,indices].T)

        # update the current source
        src = np.dot(T, src)

        # check error
        mean_error = np.mean(distances)
        if np.abs(prev_error - mean_error) < tolerance:
            break
        prev_error = mean_error

    # calculate final transformation
    T, R, _ = best_fit_transform(A, src[:m,:].T)

    return T, R, distances, src[0:2, :].T


if __name__ == '__main__':
    pair_list = [('./scan_t_10.txt', './scan_t_30.txt'),
                 ('./scan_t_30.txt', './scan_t_100.txt'),
                 ('./scan_t_100.txt', './scan_t_180.txt'),
                 ('./scan_t_10.txt', './scan_t_200.txt')
                 ]
    for i, (A_dir, B_dir) in enumerate(pair_list):
        A = pd.read_table(A_dir, header=None).to_numpy()
        B = pd.read_table(B_dir, header=None).to_numpy()
        # 随机删除一些点(50个点)
        np.random.shuffle(A)
        np.random.shuffle(B)
        A = A[0:-50]
        B = B[0:-50]

        T, R, distances, A_result = icp(A, B)
        RMSE = np.sqrt(np.mean(distances ** 2))
        print(T, '\n', R, '\n', RMSE, '\n')

        # 匹配结果图
        plt.subplot(2, 2, i+1)
        plt.scatter(A_result[:, 0], A_result[:, 1], c='b', marker='.', label='icp_result')
        plt.scatter(B[:, 0], B[:, 1], c='r', marker='.', label='target')
        A_name = os.path.basename(A_dir).split('.')[0]
        B_name = os.path.basename(B_dir).split('.')[0]
        plt.title(A_name+'---'+B_name)
        plt.legend()

        plt.show()

