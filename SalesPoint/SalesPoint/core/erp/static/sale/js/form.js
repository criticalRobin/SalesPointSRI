var vents = {
    items: {
        client: '',
        date_sale: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva = parseFloat($('select[name="iva"]').val());
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.amount * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * (iva / 100);
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    list: function () {
        this.calculate_invoice();
        $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: true,
            destroy: true,
            deferRender: true,
            data: this.items.products,
            columns: [
                { "data": "id" },
                { "data": "name" },
                { "data": "category.name" },
                { "data": "pvp" },
                { "data": "amount" },
                { "data": "subtotal" },
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3, -1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="amount" class="form-control form-control-sm" autocomplete="off" value="' + data + '">';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    }
};

$(function () {
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.amount = 1;
            ui.item.subtotal = 0.00;
            console.log(vents.items);
            vents.items.products.push(ui.item);
            vents.list();
            $(this).val('');
        }
    });
});