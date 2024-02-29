import PyPDF2


def pdf_split(split_file):
    # 读取原始的PDF文件
    pdf_reader = PyPDF2.PdfReader(split_file)

    # 获取原始文件中的总页数
    total_pages = len(pdf_reader.pages)

    # 创建一个空列表，用于存放新创建的PDF文件名
    new_files = []

    # 循环遍历每一页
    for i in range(total_pages):
        # 创建一个新的PdfFileWriter对象
        pdf_writer = PyPDF2.PdfWriter()
        # 获取当前页对象
        page = pdf_reader.pages[i]
        # 将当前页对象添加到PdfFileWriter对象中
        pdf_writer.add_page(page)
        # 创建一个新的PDF文件名，格式为"original_页码.pdf"
        new_file = f"original_{i+1}.pdf"
        # 将新的PDF文件名添加到列表中
        new_files.append(new_file)
        # 打开一个新的PDF文件，以二进制写入模式
        with open(new_file, "wb") as f:
            # 将PdfFileWriter对象中的内容写入到新的PDF文件中
            pdf_writer.write(f)

    # 打印出新创建的PDF文件名
    print(new_files)

def pdf_merge(merge_file_num):
    # 创建一个PdfMerger对象
    pdf_merger = PyPDF2.PdfMerger()

    # 创建一个空列表，用于存放要合并的PDF文件名
    files_to_merge = []

    # 循环遍历要合并的5个小文件
    for i in range(merge_file_num):
        # 获取当前小文件名，格式为"original_页码.pdf"
        file = f"original_{i+1}.pdf"
        # 将当前小文件名添加到列表中
        files_to_merge.append(file)
        # 用PdfFileReader对象打开当前小文件
        pdf_reader = PyPDF2.PdfReader(file)
        # 用PdfFileMerger对象添加当前小文件，append方法可以将所有页面添加到合并器中
        pdf_merger.append(pdf_reader)

    # 创建一个新的PDF文件名，格式为"original_merged.pdf"
    new_file = "original_merged.pdf"

    # 打开一个新的PDF文件，以二进制写入模式
    with open(new_file, "wb") as f:
        # 将PdfFileMerger对象中的内容写入到新的PDF文件中
        pdf_merger.write(f)

    # 打印出新创建的PDF文件名
    print(new_file)
if __name__ == '__main__':
    # pdf_split('9月.pdf')
    pdf_merge(12)
    
