from aiogram import Router
from aiogram import types, F
from keyboards.work_k import next_buttons, generate_categ_kb, cancel_add, is_expence_repl
from aiogram.filters import StateFilter
from repositoies.category import CategoryRepo
from repositoies.user import UserRepo
from aiogram.fsm.context import FSMContext
from states.category_state import AddCategoryState
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hitalic

router = Router()

@router.callback_query(F.data == 'categories')
async def go_to_category(callback: types.CallbackQuery, category_repo: CategoryRepo, user_repo: UserRepo):
    await callback.answer()

    user = await user_repo.get_user_by_tg_id(callback.from_user.id)

    #получаем список категорий пользователя

    req = await category_repo.get_list_by_user_id(user.id)

    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=generate_categ_kb(req)
    )

@router.callback_query(F.data == 'add_category')
async def add_new_category_action(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        'Введите название категории:', reply_markup=cancel_add()
    )

    await state.set_state(AddCategoryState.NAME_CATEGORY)


@router.callback_query(StateFilter(AddCategoryState), F.data == 'break_add')
async def cancel_add_new_category(callback: types.CallbackQuery, state: FSMContext, user_repo: UserRepo, category_repo: CategoryRepo):
    await callback.answer("Добавление отменено")
    await state.clear()

    await callback.answer()

    user = await user_repo.get_user_by_tg_id(callback.from_user.id)

    #получаем список категорий пользователя

    req = await category_repo.get_list_by_user_id(user.id)

    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=generate_categ_kb(req)
    )


@router.message(AddCategoryState.NAME_CATEGORY)
async def user_new_category(message: types.Message, 
                           state: FSMContext,):
    if message.text.isdigit():
        await message.answer('Введите название категории, а не цифры')
        return
    
    await state.update_data(category_name=message.text)
    
    await message.answer(f'Выберите тип категории:', reply_markup=is_expence_repl())
    await state.set_state(AddCategoryState.TYPE_CATEGORY)

@router.message(StateFilter(AddCategoryState.TYPE_CATEGORY))
async def add_is_expense_true(message: types.Message, 
                              state: FSMContext, 
                              user_repo: UserRepo,
                              category_repo: CategoryRepo):
    
    if message.text == '💰Доход':
        is_expence = False
    elif message.text == '💸Расход':
        is_expence = True
    else:
        await message.answer('Выберите тип из предложенных ниже вариантов')
        return 



    try:
        state_data = await state.get_data()
        category_name = state_data.get("category_name")

        if not category_name:
            await message.answer("Не найдено имя категории")
            await state.clear()


        user = await user_repo.get_user_by_tg_id(message.from_user.id)

        await category_repo.add_new_category(category_name, user.id, is_expence)
        await message.answer('Категория успешно добавлена', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        
        categories = await category_repo.get_list_by_user_id(user.id)

        if categories:

            category_list = '\n'.join([f'• {cat.name}' for cat in categories])

            await message.answer(
                f"📁 {hbold('Ваши категории:')}\n\n"
                f"{category_list}\n\n"
                f"{hitalic('Выберите категорию:')}",
                reply_markup=generate_categ_kb(categories),
                parse_mode="HTML"
            )


    except Exception as e:

        await message.answer(f'Ошибка {str(e)} обратитесь к администратору', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        






    