from aiogram import Router, types
from aiogram.types import InputFile
import os
import aiofiles.os

message_router = Router()


async def download_pdf(bot, file_id, destination):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    await bot.download_file(file_path, destination=destination)


async def delete_files(filenames):
    for filename in filenames:
        try:
            await aiofiles.os.remove(filename)
        except FileNotFoundError:
            pass

#
# @message_router.message()
# async def convert_pdf_to_images(message: types.Message):
#     if message.document.mime_type != "application/pdf":
#         return
#
#     pdf_filename = f"{message.document.file_name}"
#     await download_pdf(message.bot, message.document.file_id, pdf_filename)
#
#     try:
#         pdf_document = fitz.open(pdf_filename)
#     except Exception as e:
#         await message.reply(f"An error occurred while opening the PDF: {e}")
#         return
#
#     num_pages = pdf_document.page_count
#     image_filenames = []
#
#     for i in range(num_pages):
#         page = pdf_document[i]
#         image = page.get_pixmap()
#         image_filename = f'out_{i}.png'
#         image.save(image_filename)
#         image_filenames.append(image_filename)
#
#     media = [types.InputMediaPhoto(media=InputFile(img)) for img in image_filenames]
#     await message.bot.send_media_group(message.chat.id, media)
#
#     pdf_document.close()
#     await delete_files([pdf_filename] + image_filenames)


# @message_router.message()
# async def convert_webpage_to_pdf(message: types.Message):
#     url = message.text
#     pdf_filename = 'out.pdf'
#
#     try:
#         path_pdfkit = r"C:\Users\User\Desktop\NAJOT TA'LIM\Darslar\registration_bot\wkhtmltopdf\bin\wkhtmltopdf.exe"
#         pdfkit_options = {
#             'quiet': '',
#             'path': path_pdfkit
#         }
#         pdfkit.from_url(url, pdf_filename, options=pdfkit_options)
#         with open(pdf_filename, 'rb') as file:
#             await message.bot.send_document(message.chat.id, file, caption="Here is your PDF!")
#     except Exception as e:
#         await message.reply(f"An error occurred: {e}")
#     finally:
#         await delete_files([pdf_filename])
