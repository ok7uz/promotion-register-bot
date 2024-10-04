import io
import os

import pandas as pd
from PIL import Image as PILImage
from openpyxl.drawing.image import Image

from bot.misc import bot


async def save_to_excel(df: pd.DataFrame, file_name: str) -> None:
    """
    Save a DataFrame to an Excel file with embedded images.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_name (str): The name of the Excel file to save.

    """
    try:
        # Drop the 'file_id' column for the DataFrame to be saved
        df_without_file_id = df.drop(columns=['file_id'])
        
        # Create an Excel writer using openpyxl engine
        with pd.ExcelWriter(file_name, engine='openpyxl') as excel_writer:
            df_without_file_id.to_excel(excel_writer, index=False, sheet_name='Promos')
            workbook = excel_writer.book
            worksheet = workbook['Promos']

            # Set column widths
            img_width = 80
            worksheet.column_dimensions['A'].width = 25
            worksheet.column_dimensions['B'].width = 15
            worksheet.column_dimensions['C'].width = 50
            worksheet.column_dimensions['D'].width = 15
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = img_width // 8

            # Add images to the worksheet
            for index, row in df.iterrows():
                file_id = row.get('file_id')
                if file_id:
                    try:
                        file = await bot.get_file(file_id)
                        image = await bot.download_file(file.file_path)
                        temp_image_name = f'temp_{index}.png'
                        if image:
                            img = PILImage.open(image)
                            img.thumbnail((img.height // 3, img.width // 3), PILImage.Resampling.LANCZOS)
                            img.save(temp_image_name)

                            img = Image(temp_image_name)
                            old_width = img.width
                            img.width = img_width
                            img.height = int(img.height * img.width / old_width)
                            img.anchor = f'F{index + 2}'
                            worksheet.add_image(img)
                            worksheet.row_dimensions[index + 2].height = img.height * 3 // 4
                        # os.remove(temp_image_name)
                    except Exception as e:
                        print(f"Failed to process image for file_id {file_id}: {e}")

    except Exception as e:
        print(f"Failed to save DataFrame to Excel: {e}")
        raise
