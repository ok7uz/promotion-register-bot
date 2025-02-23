import io
import asyncio

from loguru import logger
import pandas as pd
from pathlib import Path
from PIL import Image as PILImage
from openpyxl.drawing.image import Image
from datetime import date, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from bot.misc import bot

MAX_IMAGE_SIZE = (800, 800)
TEMP_DIR  = 'temp_images'
CHUNK_SIZE = 10


async def process_single_image(file_id: str, index: int, temp_dir: str) -> str:
    temp_image_path = Path(temp_dir) / f'temp_{index}.png'

    try:
        image_data = await bot.download_file(file_id)

        with PILImage.open(image_data) as img:
            # Resize image maintaining aspect ratio
            img.thumbnail(MAX_IMAGE_SIZE, PILImage.Resampling.LANCZOS)
            # Save with optimization
            img.save(
                temp_image_path,
                "PNG",
                optimize=True,
                quality=85
            )
        
        return str(temp_image_path)
    
    except Exception as e:
        logger.error(f"Error processing image {file_id}: {e}")
        return None


async def save_to_excel(df: pd.DataFrame, file_name: str) -> None:
    temp_dir = Path(TEMP_DIR)
    temp_dir.mkdir(exist_ok=True)

    try:
        # Drop the 'file_id' column for the DataFrame to be saved
        df_without_file_id = df.drop(columns=['file_id'])

        image_paths = []
        file_ids = df['file_id'].dropna().tolist()

        for i in range(0, len(file_ids), CHUNK_SIZE):
            chunk = file_ids[i:i + CHUNK_SIZE]
            tasks = [
                process_single_image(fid, idx + i, temp_dir)
                for idx, fid in enumerate(chunk)
            ]
            chunk_results = await asyncio.gather(*tasks)
            image_paths.extend(chunk_results)
        
        # Create an Excel writer using openpyxl engine
        with pd.ExcelWriter(file_name, engine='openpyxl') as excel_writer:
            df_without_file_id.to_excel(excel_writer, index=False, sheet_name='Promos')
            workbook = excel_writer.book
            worksheet = workbook['Promos']

            column_widths = {
                'A': 25, 'B': 15, 'C': 50,
                'D': 15, 'E': 15, 'F': 10
            }
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width

            img_width = 80

            for idx, img_path in enumerate(image_paths):
                if img_path:
                    try:
                        img = Image(img_path)
                        old_width = img.width
                        img.width = img_width
                        img.height = int(img.height * img.width / old_width)
                        img.anchor = f'F{idx + 2}'
                        worksheet.add_image(img)
                        worksheet.row_dimensions[idx + 2].height = img.height * 3 // 4
                    except Exception as e:
                        logger.error(f"Error adding image to Excel: {e}")
    
    except Exception as e:
        logger.error(f"Failed to save DataFrame to Excel: {e}")
        raise
    
    finally:
        # Cleanup temp files
        try:
            for file in temp_dir.glob("temp_*.png"):
                file.unlink()
            temp_dir.rmdir()
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")


MONTHS = [
    'Yanvar', 'Fevral', 'Mart', 'Aprel',
    'May', 'Iyun', 'Iyul', 'Avgust',
    'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr'
]


def create_month_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard with last 3 months"""
    today = date.today()
    keyboard = []
    
    for i in range(3):
        # Get previous month
        current_date = today.replace(day=1) - timedelta(days=1) * (i * 30)
        month_name = MONTHS[current_date.month - 1]
        callback_data = f"month:{current_date.month}:{current_date.year}"
        
        keyboard.append([
            InlineKeyboardButton(
                text=month_name,
                callback_data=callback_data
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)