import numpy as np

# def convolution_3d(input, kernel, bias):
#     input_shape = input.shape
#     kernel_shape = kernel.shape
#     output_shape = (
#     input_shape[0] - kernel_shape[0] + 1, input_shape[1] - kernel_shape[1] + 1, input_shape[2] - kernel_shape[2] + 1)
#
#     print("Input Tensor Shape:", input_shape)
#     print("Kernel Tensor Shape:", kernel_shape)
#     print("Output Tensor Shape:", output_shape)
#     output_tensor = np.zeros(output_shape)
#
#     for k in range(output_shape[2]):
#         for i in range(output_shape[0]):
#             for j in range(output_shape[1]):
#                 # output_value = np.sum(input[i:i + kernel_shape[0], j:j + kernel_shape[1], k] * kernel[:, :, k])
#
#                 # output_tensor[i, j, k] = output_value
#                 # Extract the corresponding input slice
#                 input_slice = input[i:i + kernel_shape[0], j:j + kernel_shape[1], k:k + kernel_shape[2]]
#                 # Perform element-wise multiplication with the kernel
#                 element_wise_product = input_slice * kernel
#                 # Calculate the sum of the products
#                 output_value = np.sum(element_wise_product)
#                 print(f"i: {i}, j: {j}, k: {k}")
#                 output_tensor[i, j, k] = output_value
#
#     output_tensor += bias  # Add the bias to all elements of the output tensor
#
#     return output_tensor

import numpy as np

def convolution_3d(input, kernels, bias):
    input_shape = input.shape
    num_kernels, kernel_depth, kernel_height, kernel_width = kernels.shape
    output_shape = (
        input_shape[0] - kernel_depth + 1,
        input_shape[1] - kernel_height + 1,
        input_shape[2] - kernel_width + 1,
        num_kernels
    )

    print("Input Tensor Shape:", input_shape)
    print("Kernels Tensor Shape:", kernels.shape)
    print("Output Tensor Shape:", output_shape)
    output_tensor = np.zeros(output_shape)

    for k in range(num_kernels):
        for z in range(output_shape[3]):  # Depth dimension
            for i in range(output_shape[0]):  # Height dimension
                for j in range(output_shape[1]):  # Width dimension
                    # Extract the corresponding input slice
                    input_slice = input[i:i + kernel_depth, j:j + kernel_height, z:z + kernel_width]
                    # Perform element-wise multiplication with the kernel
                    element_wise_product = input_slice * kernels[k]
                    # Calculate the sum of the products
                    output_value = np.sum(element_wise_product)
                    # print(f"Kernel: {k}, i: {i}, j: {j}, z: {z}")
                    output_tensor[i, j, z, k] = output_value

    output_tensor += bias  # Add the bias to all elements of the output tensor

    return output_tensor



def save_tensor_to_bin(tensor, filename_prefix):
    # 获取张量的形状
    shape_str = "x".join(map(str, tensor.shape))

    # 构建文件名
    filename = f"{filename_prefix}_{shape_str}.bin"

    # 保存张量为 .bin 文件
    tensor.tofile(filename)


def main():
    input_tensor = np.array([[[1, 2, 3, 4],
                              [5, 6, 7, 8],
                              [9, 10, 11, 12],
                              [13, 14, 15, 16]],
                             [[17, 18, 19, 20],
                              [21, 22, 23, 24],
                              [25, 26, 27, 28],
                              [29, 30, 31, 32]],
                             [[33, 34, 35, 36],
                              [37, 38, 39, 40],
                              [41, 42, 43, 44],
                              [45, 46, 47, 48]]])

    # 原始3D卷积核
    # 创建一个4D卷积核，第一维度为2，其它三个维度为3x3x2
    kernel_tensor = np.ones((2, 3, 3, 2))  # 使用np.ones赋予初始值为1

    bias_tensor = np.array([[[2]]])

    output = convolution_3d(input_tensor, kernel_tensor, bias_tensor)
    print("输出张量:")
    print(output)


    # 保存张量到文件
    save_tensor_to_bin(input_tensor, "input_tensor")
    save_tensor_to_bin(kernel_tensor, "kernel_tensor")
    save_tensor_to_bin(bias_tensor, "bias_tensor")
    save_tensor_to_bin(output, "output_tensor")

if __name__ == "__main__":
    main()
