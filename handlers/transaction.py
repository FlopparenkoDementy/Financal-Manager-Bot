from aiogram import Router
from aiogram import types, F
from repositoies.category import CategoryRepo
from repositoies.user import UserRepo
from aiogram.fsm.context import FSMContext
from keyboards.work_k import CategoryCallback
from states.transaction_state import TransactionForm
from repositoies.transaction import TransationRepo
from aiogram.filters import StateFilter
from keyboards.tran_kb import get_transaction_keyboards
from keyboards.tran_kb import add_trans

router = Router()

@router.callback_query(CategoryCallback.filter())
async def start_transaction(callback: types.CallbackQuery, 
                            callback_data: CategoryCallback,
                            tran_repo: TransationRepo,
                            category_repo: CategoryRepo, 
                            state: FSMContext):
    print(f"🎯 DEBUG: CategoryCallback ОБРАБОТЧИК ВЫЗВАН!")
    print(f"   📞 callback.data = '{callback.data}'")
    print(f"   🆔 callback_data.id = {callback_data.id}")
    print(f"   📊 Тип callback_data: {type(callback_data)}")
    
    has_transaction = await tran_repo.get_transactions_by_category_id(category_id=callback_data.id)

    
    category_name = await category_repo.get_category_name(callback_data.id)

    await state.update_data(category_id=callback_data.id,
                            category_name=category_name
                            )

    if len(has_transaction) > 0:
        transactions = await tran_repo.get_transactions_by_category_id(callback_data.id)
        
        msg = f"📊 В категории <b>{category_name}</b> уже есть {len(transactions)} транзакций\n"
        msg += f"Последняя: {transactions[0].amount:.2f}\n\n"
        msg += "Cоздать новую? Выберите Да или Нет\n"
        await state.set_state(TransactionForm.CONTINUE)

        
        await callback.message.answer(msg, parse_mode="HTML", reply_markup=get_transaction_keyboards().yes_or_no)


    else:
        await state.set_state(TransactionForm.WAITING_FOR_AMOUNT)

        
        
        await callback.message.answer(
            f'📝 <b>Создание новой транзакции</b>\n\n'
            f'Категория: <b>{category_name}</b>\n\n'
            f'Введите сумму:',
            parse_mode='HTML',
            reply_markup=get_transaction_keyboards().cancel_kb
        )
        
        await callback.answer()

@router.callback_query(StateFilter(TransactionForm.CONTINUE), F.data == 'dont')
async def dont_next(callback: types.CallbackQuery, 
                    tran_repo: TransationRepo,  # ✅ Убрал callback_data
                    state: FSMContext):  # ✅ Получаем состояние
    
    # ✅ Получаем данные из состояния
    data = await state.get_data()
    category_id = data.get('category_id')
    category_name = data.get('category_name')
    
    if not category_id:
        await callback.answer("Ошибка: категория не найдена")
        return
    
    transactions = await tran_repo.get_transactions_by_category_id(category_id)
    
    await state.clear()
    await show_transactions_with_add_button(
        callback=callback, 
        transactions=transactions,
        category_id=category_id,
        category_name=category_name
    )
    
    await callback.answer()


@router.callback_query(StateFilter(TransactionForm.CONTINUE), F.data == 'do')
async def do_next(callback: types.CallbackQuery, state: FSMContext):
    
    # ✅ Получаем название категории из состояния
    data = await state.get_data()
    category_name = data.get('category_name', 'Категория')
    
    await state.set_state(TransactionForm.WAITING_FOR_AMOUNT)
    
    await callback.message.answer(
        f'📝 <b>Создание новой транзакции</b>\n\n'
        f'Категория: <b>{category_name}</b>\n\n'  # ✅ Добавил название
        f'Введите сумму:',
        parse_mode='HTML',
        reply_markup=get_transaction_keyboards().cancel_kb
    )
    
    await callback.answer()






@router.message(TransactionForm.WAITING_FOR_AMOUNT)
async def process_amount(message: types.Message, state: FSMContext):
    """Обработка ввода суммы"""

    try:

        amount = float(message.text.replace(',', '.'))

        if amount <= 0:
            await message.answer("Сумма должна быть больше 0!", reply_markup=get_transaction_keyboards().cancel_kb)
            return
        
        await state.update_data(amount=amount)

        await state.set_state(TransactionForm.WAITING_FOR_DESCR)

        await message.answer(
            f'✅ Сумма: <b>{amount:.2f}</b>\n\n'
            f'Введите описание транзакции (не более 250 символов) или нажмите "Пропустить"',
            parse_mode='HTML',
            reply_markup=get_transaction_keyboards().skip_kb
        )

    except ValueError:
        await message.answer(
            'Введите корректное число! (1500 или 1499.99)',
            reply_markup=get_transaction_keyboards().cancel_kb
        )

@router.message(TransactionForm.WAITING_FOR_DESCR)
async def process_descrpition(message: types.Message, 
                              state: FSMContext, 
                              ):

    descr = message.text

    if descr == 'Пропустить':
        descr = 'Без описания'

    await state.update_data(descr=descr)

    await state.set_state(TransactionForm.CONFIRM)

    data = await state.get_data()

    await message.answer(
        f"📋 <b>Подтвердите данные транзакции:</b>\n\n"
        f"💰 Сумма: <b>{data['amount']:.2f}</b>\n"
        f"📁 Категория: <b>{data.get('category_name', 'Не указана')}</b>\n"
        f"📝 Описание: <b>{data['descr']}</b>\n\n"
        f"Все верно?",
        parse_mode="HTML",
        reply_markup=get_transaction_keyboards().confirmation_kb
    )


@router.callback_query(TransactionForm.CONFIRM, F.data.in_(['confirm', 'cancel']))
async def process_confirmation(callback: types.CallbackQuery, 
                               state: FSMContext, 
                               tran_repo: TransationRepo,
                               user_repo: UserRepo):
    
    
    if callback.data == 'confirm':
        data = await state.get_data()

        user = await user_repo.get_user_by_tg_id(callback.from_user.id)

        transaction = await tran_repo.save_transaction_to_db(data, user.id)

        await state.clear()

        await callback.message.answer(
            f"✅ <b>Транзакция успешно сохранена!</b>\n\n"
            f"ID: {transaction.id}\n"
            f"Сумма: {transaction.amount:.2f}\n"
            f"Категория: {data['category_name']}\n"
            f"Дата: {transaction.created.strftime('%d.%m.%Y %H:%M')}",
            parse_mode="HTML"
        )

    else:
        await state.clear()

        await callback.message.answer(
            '❌ Создание транзакции отменено.'
        )

        await callback.answer()


@router.callback_query(TransactionForm.WAITING_FOR_AMOUNT, F.data == 'cancel_transaction')
async def process_cancel(callback: types.CallbackQuery, state: FSMContext, tran_repo: TransationRepo):
    """Обработчик отмены создания транзакции"""
    # ✅ Получаем данные из состояния
    data = await state.get_data()
    category_id = data.get('category_id')
    category_name = data.get('category_name')
    
    if not category_id:
        await callback.answer("Ошибка: категория не найдена")
        return
    
    transactions = await tran_repo.get_transactions_by_category_id(category_id)
    
    await state.clear()
    await show_transactions_with_add_button(
        callback=callback, 
        transactions=transactions,
        category_id=category_id,
        category_name=category_name
    )
    
    await callback.answer()

async def show_transactions_with_add_button(callback: types.CallbackQuery,
                                            transactions: list,
                                            category_id: int,
                                            category_name: str):
    """Показать транзакции с кнопкой для добавления новой"""
    
    message_text = f"📊 <b>{category_name}</b> - транзакции:\n\n"
    
    total = 0
    for i, trans in enumerate(transactions[:5], 1):
        date_str = trans.created.strftime('%d.%m.%Y %H:%M') if hasattr(trans, 'created') else ''
        desc = trans.description[:20] + "..." if trans.description and len(trans.description) > 20 else (trans.description or "")
        message_text += f"{i}. {date_str}: <b>{trans.amount:.2f}</b> - {desc}\n"
        total += trans.amount
    
    if len(transactions) > 5:
        message_text += f"\n... и еще {len(transactions) - 5} транзакций\n"
    elif len(transactions) == 0:
        message_text += f'\nПока нет транзакций'
    
    message_text += f"\n<b>Всего: {total:.2f}</b>"
    
    # Отправляем ОДНО сообщение
    await callback.message.answer(message_text, parse_mode='HTML', reply_markup=add_trans(category_id=category_id))