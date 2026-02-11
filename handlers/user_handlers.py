from time import sleep

from aiogram import Bot, F, Router
from aiogram.types import InputFile
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile




from keyboards.main_menu import get_main_menu
from keyboards.resolutions_kb import create_resolutions_keyboard
from config_data.config import Config, load_config
from services.tools import get_video_info, download_video, move_downloaded_file

router = Router()
config: Config = load_config()

storage = MemoryStorage()

class FSMVideo(StatesGroup):
    download_video = State()

@router.message(~F.text)
async def content_type_example(msg: Message):
    await msg.answer('👍')


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
        await message.answer(
        text='Hello message',
        reply_markup=get_main_menu())


@router.message(F.text(text='Button 1'))
async def process_button_1_command(message: Message):
    await message.answer(
         text='Button 1 pressed', 
         reply_markup=get_main_menu()
    )


@router.message(F.text, StateFilter(default_state))
async def process_get_url_command(callback: CallbackQuery, state: FSMContext):
    print('URL recieved')
    url = callback.text
    video_info = get_video_info(url)
    is_short = video_info['is_short']
    resolutions = video_info['uniq_v_resolutions'] if is_short else video_info['uniq_h_resolutions']
    resolutions.sort()
    resolutions = [resolution + 'p' for resolution in resolutions]
    resolution_word = 'вертикальное' if is_short else 'горизонтальное'

    message_text = f"""
{video_info['title']}
Длительность: {video_info['duration']}
Просмотры: {video_info['view_count']}
Лайки: {video_info['like_count']}
Дата загрузки: {video_info['upload_date']}

Для загрузки видео выберите {resolution_word} разрешение:
"""
    
    await state.update_data(url=url)
    await state.update_data(is_short=is_short)
    
    await callback.answer_photo(
         photo=video_info['thumbnail'],
         caption=message_text,
         reply_markup=create_resolutions_keyboard(*resolutions)
    )
    await state.set_state(FSMVideo.download_video)


@router.callback_query(F.data, StateFilter(FSMVideo.download_video))
async def process_download_video(callback: CallbackQuery, state: FSMContext):
    print('Handled')
    resolution = callback.data[:-1]
    video_dict = await state.get_data()
    url = video_dict['url']
    is_short = video_dict['is_short']
    id = callback.from_user.id
    try:
        output_file_path = download_video(url, resolution, is_short, id)
        print(output_file_path)
        # Чтение файла и создание объекта InputFile одним действием
        with open(output_file_path, 'rb'):
            input_file = FSInputFile(output_file_path)
            await callback.message.answer_video(
                video=input_file,
                caption=f'Видео скачано в разрешении {resolution}p',
                reply_markup=get_main_menu()
            )
            move_downloaded_file(output_file_path)
            await state.clear()
    except Exception as e:
                print(f'Exception in proccess download video: {e}')
                await callback.message.answer(
                    text='Произошла ошибка при загрузке или отправке видео. Попробуйте повторить.',
                    reply_markup=get_main_menu()
                )
                await state.clear()
