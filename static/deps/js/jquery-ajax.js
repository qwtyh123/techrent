$(document).ready(function () {
    // Элемент для оповещений от AJAX
    var successMessage = $("#jq-notification");

    // Обработчик клика по кнопке "Добавить в корзину"
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();
        var goodsInCartCount = $("#goods-in-cart-count");
        var product_id = $(this).data("product-id");
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                action: 'increase' // Добавляем действие для увеличения
            },
            success: function (data) {
                successMessage.html(data.message).fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Обновляем количество товаров в корзине
                goodsInCartCount.text(data.quantity);
                $("#cart-items-container").html(data.cart_items_html);
            },
            error: function () {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    // Обработчик клика по кнопке "Удалить из корзины"
    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();
        var goodsInCartCount = $("#goods-in-cart-count");
        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                action: 'decrease' // Добавляем действие для уменьшения
            },
            success: function (data) {
                successMessage.html(data.message).fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                goodsInCartCount.text(data.quantity); // Обновляем отображение количества товаров
                $("#cart-items-container").html(data.cart_items_html); // Обновляем содержимое корзины
            },
            error: function () {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });

    // Обработчик для уменьшения количества товара на 30
    $(document).on("click", ".decrement", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");

        updateCart(cartID, 'decrease', url); // Отправляем AJAX-запрос с действием уменьшения
    });

    // Обработчик для увеличения количества товара на 30
    $(document).on("click", ".increment", function () {
        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");

        updateCart(cartID, 'increase', url); // Отправляем AJAX-запрос с действием увеличения
    });

    // Функция обновления корзины
    function updateCart(cartID, action, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                action: action // Передаем действие (increase или decrease)
            },
            success: function (data) {
                successMessage.html(data.message).fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                var goodsInCartCount = $("#goods-in-cart-count");

                goodsInCartCount.text(data.quantity); // Обновляем отображение количества товаров

                $("#cart-items-container").html(data.cart_items_html); // Обновляем содержимое корзины
            },
            error: function () {
                console.log("Ошибка при обновлении корзины");
            },
        });
    }

    // Удаление уведомления через 7 секунд
    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    // Открытие модального окна корзины
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body').modal('show');
    });

    // Закрытие модального окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // Обработчик выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        if ($(this).val() === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });

    // Форматирования ввода номера телефона в форме (xxx) xxx-хххx
    document.getElementById('id_phone_number').addEventListener('input', function (e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    // Проверяем на стороне клинта коррекность номера телефона в форме xxx-xxx-хх-хx
    $('#create_order_form').on('submit', function (event) {
        var phoneNumber = $('#id_phone_number').val();
        var regex = /^\(\d{3}\) \d{3}-\d{4}$/;

        if (!regex.test(phoneNumber)) {
            $('#phone_number_error').show();
            event.preventDefault();
        } else {
            $('#phone_number_error').hide();

            // Очистка номера телефона от скобок и тире перед отправкой формы
            var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
            $('#id_phone_number').val(cleanedPhoneNumber);
        }
    });
});