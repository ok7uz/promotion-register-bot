import pandas as pd
from openpyxl.drawing.image import Image

from bot.misc import bot


async def save_to_excel(df, file_name):
    df_without_file_id = df.drop(columns=['file_id'])

    excel_writer = pd.ExcelWriter(file_name, engine='openpyxl')
    df_without_file_id.to_excel(excel_writer, index=False, sheet_name='Promos')

    workbook = excel_writer.book
    worksheet = workbook['Promos']
    img_width = 80
    worksheet.column_dimensions['A'].width = 25
    worksheet.column_dimensions['B'].width = 15
    worksheet.column_dimensions['C'].width = 50
    worksheet.column_dimensions['D'].width = 15
    worksheet.column_dimensions['E'].width = 15
    worksheet.column_dimensions['F'].width = img_width

    for index, row in df.iterrows():
        file_id = row['file_id']
        file = await bot.get_file(file_id)
        image = await bot.download_file(file.file_path)
        if image:
            img = Image(image)
            old_width = img.width
            img.width = img_width
            img.height = int(img.height * img.width / old_width)
            img.anchor = f'F{index + 2}'
            worksheet.add_image(img)
            worksheet.row_dimensions[index + 2].height = img.height

    excel_writer.close()
