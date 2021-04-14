"""
# PDF Freeze v1.0.0
by robinoms 2021

Digital print-and-scan of PDF documents. 
Converts a PDF into JPG, then back to PDF. 
This makes your confidential PDFs slightly more secure.

* Signatures made trough Adobe Acrobat become more difficult to copy/steal. 
* The text becomes static and more difficult to alter/fake. 

## Dependencies

!!! warning
    poppler must be installed on the system.

### poppler Windows Installation

* Download pre-compiled windows-release of poppler:
    * See: [oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases/).
* Extract the downloaded files. 
* Place the files somewhere nice. 
    * For example, place the files so that doppler's bin folder can be located here: 'C:\Program Files\poppler\poppler-x.x.x\bin'
        * Replace x.x.x with the version number of the one you downloaded. 
* Add the path of poppler's bin folder to the system's Path environment variable. 
    * Press start
    * Search "environment"
    * Press "Edit the system environment variables"
    * Go to the "Advanced" tab. 
    * Press "Environment Variables"
    * Edit the "Path" variable under User variables. 
    * Click on "new" and insert the path to poppler's bin folder (e.g. 'C:\Program Files\poppler\poppler-x.x.x\bin')
    * Hit "OK", then "OK"

You can verify the installation by typing in the command prompt:

```batch
    WHERE doppler.dll
```

If the system is able to locate doppler.dll, then doppler has been successfully installed on your system. 

### Other Dependencies

* pdf2image
* fpdf

Both of these can be installed via pip.

## Simple Usage

From a terminal window (e.g. Command Prompt):

```batch
    python -m pdf_freeze --i original.pdf --o freezed.pdf --dpi 300
``'

(Assuming Python has been added to the user/system's Path environment variable.)

"""

import os
from pdf2image import convert_from_path
from fpdf import FPDF


TEMP_FOLDER = 'temp/'


def _make_temp_folder(path) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)

def _pdf_to_jpg(input_file: str, dpi: int) -> list:
    print(f'    converting pages to jpg...')
    pages = convert_from_path(input_file, dpi=dpi)
    page_nr = 0
    image_list = []
    print('    exporting jpgs...')
    for page in pages:
        page_nr += 1
        print(f'        page: {page_nr}/{len(pages)}')
        filename = TEMP_FOLDER + f'page_{page_nr}.jpg'
        image_list.append(filename)
        page.save(filename, 'JPEG')
    return image_list


def _jpg_to_pdf(image_list: list, output_file: str) -> bool:
    pdf = FPDF()
    print('    building final pdf...')
    for image in image_list:
        print(f'       adding page: {image}')
        pdf.add_page()
        pdf.image(name=image, x=0, y=0, w=210, h=297)
    print('    exporting final pdf...')
    pdf.output(output_file, "F")


def main(input_file: str, output_file: str, dpi: int) -> None:
    print('~ PDF FREEZE ~')
    if not os.path.isfile(input_file):
        raise ValueError(f'unable to locate input file: {input_file}')
    _make_temp_folder(TEMP_FOLDER)
    img_list = _pdf_to_jpg(input_file, dpi)
    _jpg_to_pdf(img_list, output_file)
    print('success - pdf has been freeeeezed')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert PDF to JPG, then back to PDF')
    parser.add_argument('--i', metavar='input', required=True,
                        help='input pdf file path')
    parser.add_argument('--o', metavar='output', required=True,
                        help='output pdf file path')
    parser.add_argument('--dpi', metavar='dpi', required=False, default=300,
                        help='dots per inch - determines image quality')
    args = parser.parse_args()
    main(input_file=args.i, output_file=args.o, dpi=args.dpi)
