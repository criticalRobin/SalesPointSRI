var tblProducts;
var vents = {
    items: {
        client: '',
        date_sale: '',
        subtotalPVP: 0.00,
        subtotalSalePrice: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    calculate_invoice: function () {
        var subtotalPVP = 0.00;
        var subtotalSalePrice = 0.00;
        var without_iva = parseFloat($('select[name="iva"]').val());

        $.each(this.items.products, function (pos, dict) {
            dict.subtotalPVP = dict.amount * parseFloat(dict.pvp);
            dict.subtotalSalePrice = dict.amount * parseFloat(dict.sale_price);
            subtotalPVP += dict.subtotalPVP;
            subtotalSalePrice += dict.subtotalSalePrice;
        });

        this.items.subtotalPVP = subtotalPVP;
        this.items.subtotalSalePrice = subtotalSalePrice;

        this.items.iva = (this.items.subtotalPVP * (without_iva / 100)) + (this.items.subtotalSalePrice * (without_iva / 100));
        this.items.total = this.items.subtotalPVP + this.items.subtotalSalePrice + this.items.iva;

        $('input[name="subtotalPVP"]').val(this.items.subtotalPVP.toFixed(2));
        $('input[name="subtotalSalePrice"]').val(this.items.subtotalSalePrice.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: true,
            destroy: true,
            deferRender: true,
            data: this.items.products,
            columns: [
                { "data": "id" },
                { "data": "name" },
                { "data": "stock" },
                { "data": "pvp" },
                { "data": "amount" },
                { "data": "subtotalPVP" },
                { "data": "subtotalSalePrice" },
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
                    targets: [-4, -2, -1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="amount" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        return '<span class="badge badge-danger">' + data + '</span>'
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="amount"]').TouchSpin({
                    min: 0,
                    max: data.stock,
                    step: 1
                });
            },
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
            ui.item.subtotalPVP = 0.00;
            ui.item.subtotalSalePrice = 0.00;
            console.log(vents.items);
            vents.items.products.push(ui.item);
            vents.list();
            $(this).val('');
        }
    });

    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products.splice(tr.row, 1);
            vents.list();
        })
        .on('change keyup', 'input[name="amount"]', function () {
            console.clear();
            var amount = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].amount = amount;
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotalPVP.toFixed(2));
            $('td:eq(6)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotalSalePrice.toFixed(2));
        });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // event submit sale 
    $('form').on('submit', function (e) {
        e.preventDefault();
        if (vents.items.products.length === 0) {
            message_error('No se puede realizar una venta con 0 productos');
            return false;
        }
        vents.items.date_sale = $('input[name="date_sale"]').val();
        vents.items.client = $('select[name="client"]').val();

        vents.calculate_invoice();

        var parameters = new FormData(this);
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro de realizar la siguiente acción?', parameters, function (response) {
            // if (!response.hasOwnProperty('error')) {
            //     location.href = '/erp/venta/listado#';
            // } else {
            //     message_error(response.error);
            // }
            location.href = '/erp/venta/listado#';
        });
    });

    vents.list();
});