window.onload = function () {
    prepare_token();

    divs_hidden_by_default([
        $("#quantity-form"),
        $("#accept-form"),
        $("#trans-status"),
        $("#stats"),
        $(".up-info"),
    ]);

    let quantiles;
    let prices;

    $(".set-alarm").click(
        function () {
            $("#asset-table").hide(400);
            asset = $(this).attr("id");
            quantiles = $(this).attr("quantiles");

            prices = {
                "buy" : $(this).attr("buy"),
                "sell" : $(this).attr("sell"),
            };

            $("#quantity-form").show(500)
                .find("#qform-title")
                .html(
                    `Your alarm configuration for ${asset}`
                );
        }
    );

    $("#accept-success").click(
        function () {
            $("#trans-status").hide(500);
            $("#asset-table").show(500);
        }
    );

    function populate_success(data) {
        $("#accept-success").show(500);
        $("#loading").hide(500);
        $("#trans-status").find('#status-info').html(
            data.message
        );

    }

    function populate_error(error) {
        $("#accept-success").show(500);
        $("#loading").hide(500);
        $("#trans-status").find('#status-info').html(
            error
        );
    }

    $("#send-alert").click(function () {
        $("#quantity-form").hide(400);
        $("#stats").show(500);

        //what is the threshold?
        let threshold = $('#quantity').val();
        let price = $('input:radio[name=price]:checked').val();
        populate_chart(quantiles, threshold, price, prices[price])
    });

    $("#accept-set").click(function () {
        $("#stats").hide(400);

        //what is the selected type?
        let type = $('input:radio[name=type]:checked').val();
        //what is the price?
        let price = $('input:radio[name=price]:checked').val();
        //what is the threshold?
        let threshold = $('#quantity').val();

        $("#quantity-form").hide(400);
        $("#trans-status").show(500).find("#accept-success").hide();
        $.ajax({
            url: '',
            type: 'post',
            data: {
                'type': type,
                'price': price,
                'threshold': threshold,
                'asset': asset
            },
            success: function (data) {
                populate_success(data)
            },
            error: function (jqXHR, status, errorThrown) {
                populate_error(errorThrown)
            }

        });

    });

    $("#cancel-set").click(
        function () {
            $("#stats").hide(400);
            $("#quantity-form").show(500);
        }
    );

    $("#cancel-alert").click(
        function () {
            $("#quantity-form").hide(400);
            $("#asset-table").show(500);
        }
    );

    $("#choice1").click(
        function () {
            $(".up-info").show(400);
            $(".down-info").hide(400);
        }
    );

    $("#choice2").click(
        function () {
            $(".down-info").show(400);
            $(".up-info").hide(400);
        }
    ).click();

    $("#price_choice_1").click();

    /* --------------- RADIO ------------------*/

    const st = {};

    st.flaptype = document.querySelector('#flaptype');
    st.flapprice = document.querySelector('#flapprice');
    st.toggle = document.querySelector('.toggle');

    st.choice1 = document.querySelector('#choice1');
    st.choice2 = document.querySelector('#choice2');

    st.price_choice_1 = document.querySelector('#price_choice_1');
    st.price_choice_2 = document.querySelector('#price_choice_2');

    st.clickHandler = (e) => {

        let new_text = e.target.textContent;

        if ($(e.target).attr('class') === 'type') {
            setTimeout(() => {
                st.flaptype.children[0].textContent = new_text;
            }, 250);
        } else if ($(e.target).attr('class') === 'price') {
            setTimeout(() => {
                st.flapprice.children[0].textContent = new_text;
            }, 250);
        }



    };

    document.addEventListener('click', (e) => st.clickHandler(e));
};
