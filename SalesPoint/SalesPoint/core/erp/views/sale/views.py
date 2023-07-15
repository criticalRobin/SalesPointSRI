import json
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from SalesPoint.core.erp.models import Sale, Product, SaleDetails
from SalesPoint.core.erp.forms import SaleForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db import transaction
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
import xml.etree.ElementTree as ET
import uuid


class SaleListView(ListView):
    model = Sale
    template_name = "sale/list.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif action == "search_details_prod":
                data = []
                for i in SaleDetails.objects.filter(sale_id=request.POST["id"]):
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Ventas"
        context["create_url"] = reverse_lazy("erp:sale_create")
        context["list_url"] = reverse_lazy("erp:sale_list")
        context["entity"] = "Ventas"
        return context


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sale/create.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "search_products":
                data = []
                prods = Product.objects.filter(name__icontains=request.POST["term"], stock__gt=0)
                for i in prods[0:10]:
                    item = i.toJSON()
                    item["value"] = i.name
                    data.append(item)
            elif action == "add":
                with transaction.atomic():
                    vents = json.loads(request.POST["vents"])
                    sale = Sale()
                    date_sale_str = self.request.POST.get("date_sale")
                    date_sale = datetime.strptime(date_sale_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                    sale.date_sale = date_sale
                    sale.client_id = self.request.POST.get("client")
                    sale.save()

                    for i in vents["products"]:
                        det = SaleDetails()
                        det.price = float(i["pvp"])
                        det.amount = int(i["amount"])
                        det.product_id = i["id"]
                        det.sale = sale  # Asignar el objeto Sale a SaleDetails
                        det.save()
                        det.product.stock -= det.amount
                        det.product.save()

                    sale.calculate_total()  # Calcular subtotal y total
                    sale.save()  # Guardar Sale actualizado

                    # Actualizar los valores de subtotal y total en el formulario
                    form = self.get_form()
                    form.instance = sale
                    form.fields["subtotal"].initial = sale.subtotal
                    form.fields["total"].initial = sale.total

                    if form.is_valid():
                        form.save()
            else:
                raise Exception("El formulario no es válido")

        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creación de una Venta"
        context["list_url"] = reverse_lazy("erp:sale_list")
        context["entity"] = "Ventas"
        context["action"] = "add"
        return context


# class SaleUpdateView(UpdateView):
#     model = Sale
#     form_class = SaleForm
#     template_name = "sale/create.html"
#     success_url = reverse_lazy("erp:sale_list")
    
#     @method_decorator(csrf_exempt)
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Edición de una Venta"
#         context["list_url"] = reverse_lazy("erp:sale_list")
#         context["entity"] = "Ventas"
#         return context


# class SaleDeleteView(DeleteView):
#     model = Sale
#     template_name = "sale/delete.html"
#     success_url = reverse_lazy("erp:sale_list")
    
#     @method_decorator(csrf_exempt)
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Eliminación de una Ventas"
#         context["list_url"] = reverse_lazy("erp:sale_list")
#         context["entity"] = "Ventas"
#         return context


class SaleInvoicePdf(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    # def link_callback(self, uri, rel):
    #         """
    #         Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    #         resources
    #         """
    #         result = finders.find(uri)
    #         if result:
    #                 if not isinstance(result, (list, tuple)):
    #                         result = [result]
    #                 result = list(os.path.realpath(path) for path in result)
    #                 path=result[0]
    #         else:
    #                 sUrl = settings.STATIC_URL        # Typically /static/
    #                 sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
    #                 mUrl = settings.MEDIA_URL         # Typically /media/
    #                 mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

    #                 if uri.startswith(mUrl):
    #                         path = os.path.join(mRoot, uri.replace(mUrl, ""))
    #                 elif uri.startswith(sUrl):
    #                         path = os.path.join(sRoot, uri.replace(sUrl, ""))
    #                 else:
    #                         return uri

    #         # make sure that file exists
    #         if not os.path.isfile(path):
    #                 raise Exception(
    #                         'media URI must start with %s or %s' % (sUrl, mUrl)
    #                 )
    #         return path

    def get(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.get(pk=self.kwargs["pk"])
            # products_iva_12 = sale.details.filter(product__iva="12.00")
            # iva_12_total = sum(product.subtotal * Decimal("0.12") for product in products_iva_12)
            template = get_template("sale/invoice.html")
            context = {
                "sale": sale,
                "comp": {
                    "name": "TIENDITA S.A.",
                    "ruc": "9999999999999",
                    "address": "Su Corazón",
                },
                # "iva_12_total": iva_12_total,
            }
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            pisa_status = pisa.CreatePDF(html, dest=response)
            return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy("erp:sale_create"))
    
    
class SaleGenerateXml(View):
    def get(self, request, *args, **kwargs):
        try:
            sale_id = self.kwargs["pk"]
            sales = SaleDetails.objects.filter(sale_id=sale_id)
            
            if sales.exists():
                sale = sales.first().sale
                
                # Crear el elemento raíz del XML
                root = ET.Element("Venta")

                # Crear elementos y asignarles los valores correspondientes

                # Agregar campos adicionales
                info_tributaria = ET.SubElement(root, "infoTributaria")
                ambiente = ET.SubElement(info_tributaria, "ambiente")
                ambiente.text = "1"
                tipo_emision = ET.SubElement(info_tributaria, "tipoEmision")
                tipo_emision.text = "1"
                razon_social = ET.SubElement(info_tributaria, "razonSocial")
                razon_social.text = "LOS TILINES S.A"
                nombre_comercial = ET.SubElement(info_tributaria, "nombreComercial")
                nombre_comercial.text = "LOS TILINES S.A"
                ruc = ET.SubElement(info_tributaria, "ruc")
                ruc.text = "1805472386001"
                clave_acceso = ET.SubElement(info_tributaria, "claveAcceso")
                clave_acceso.text = "2110201101179214673900110020010000000011234567813"
                cod_doc = ET.SubElement(info_tributaria, "codDoc")
                cod_doc.text = "01"
                estab = ET.SubElement(info_tributaria, "estab")
                estab.text = "002"
                pto_emi = ET.SubElement(info_tributaria, "ptoEmi")
                pto_emi.text = "001"
                secuencial = ET.SubElement(info_tributaria, "secuencial")
                secuencial.text = "000000001"
                dir_matriz = ET.SubElement(info_tributaria, "dirMatriz")
                dir_matriz.text = "LA UTA"

                info_factura = ET.SubElement(root, "infoFactura")
                fecha_emision = ET.SubElement(info_factura, "fechaEmision")
                fecha_emision.text = str(sale.date_sale)
                dir_establecimiento = ET.SubElement(info_factura, "dirEstablecimiento")
                dir_establecimiento.text = "LA UTA"
                obligado_contabilidad = ET.SubElement(info_factura, "obligadoContabilidad")
                obligado_contabilidad.text = "SI"
                tipo_identificacion_comprador = ET.SubElement(
                    info_factura, "tipoIdentificacionComprador"
                )
                tipo_identificacion_comprador.text = "05"
                razon_social_comprador = ET.SubElement(info_factura, "razonSocialComprador")
                razon_social_comprador.text = f"{sale.client.names} {sale.client.surnames}"
                identificacion_comprador = ET.SubElement(
                    info_factura, "identificacionComprador"
                )
                identificacion_comprador.text = sale.client.dni

                # Agregar más campos adicionales
                id_compra = ET.SubElement(info_factura, "idCompra")
                id_compra.text = str(sale.pk)

                total_sin_impuestos = ET.SubElement(info_factura, "totalSinImpuestos")
                total_sin_impuestos.text = str(sale.subtotal)

                total_descuento = ET.SubElement(info_factura, "totalDescuento")
                total_descuento.text = "0.00"

                total_con_impuestos = ET.SubElement(info_factura, "totalConImpuestos")
                total_con_impuestos.text = str(sale.total)
                total_impuesto = ET.SubElement(total_con_impuestos, "totalImpuesto")
                codigo = ET.SubElement(total_impuesto, "codigo")
                codigo.text = "2"
                codigo_porcentaje = ET.SubElement(total_impuesto, "codigoPorcentaje")
                codigo_porcentaje.text = "2"
                base_imponible = ET.SubElement(total_impuesto, "baseImponible")
                base_imponible.text = "1.000"
                valor = ET.SubElement(total_impuesto, "valor")
                valor.text = "0.12"

                propina = ET.SubElement(info_factura, "propina")
                propina.text = "0.00"

                importe_total = ET.SubElement(info_factura, "importeTotal")
                importe_total.text = "1.00"

                moneda = ET.SubElement(info_factura, "moneda")
                moneda.text = "DOLAR"

                pagos = ET.SubElement(info_factura, "pagos")
                pago = ET.SubElement(pagos, "pago")
                forma_pago = ET.SubElement(pago, "formaPago")
                forma_pago.text = "01"
                total_pago = ET.SubElement(pago, "total")
                total_pago.text = str(sale.total)
                plazo = ET.SubElement(pago, "plazo")
                plazo.text = "30"
                unidad_tiempo = ET.SubElement(pago, "unidadTiempo")
                unidad_tiempo.text = "dias"

                detalles = ET.SubElement(root, "detalles")
                for sale_detail in sales:
                    detalle = ET.SubElement(detalles, "detalle")
                    codigo_principal = ET.SubElement(detalle, "codigoPrincipal")
                    codigo_principal.text = str(uuid.uuid4())[:8]
                    descripcion = ET.SubElement(detalle, "descripcion")
                    descripcion.text = sale_detail.product.name
                    cantidad = ET.SubElement(detalle, "cantidad")
                    cantidad.text = str(sale_detail.amount)
                    precio_unitario = ET.SubElement(detalle, "precioUnitario")
                    precio_unitario.text = str(sale_detail.price)
                    descuento = ET.SubElement(detalle, "descuento")
                    descuento.text = "0.00"  # Puedes ajustar este valor según tus necesidades
                    precio_total_sin_impuesto = ET.SubElement(detalle, "precioTotalSinImpuesto")
                    precio_total_sin_impuesto.text = str(sale_detail.subtotal)
                    impuestos = ET.SubElement(detalle, "impuestos")
                    impuesto = ET.SubElement(impuestos, "impuesto")
                    codigo_impuesto = ET.SubElement(impuesto, "codigo")
                    codigo_impuesto.text = (
                        "2"  # Puedes ajustar este valor según tus necesidades
                    )
                    codigo_porcentaje_impuesto = ET.SubElement(impuesto, "codigoPorcentaje")
                    codigo_porcentaje_impuesto.text = (
                        "2"  # Puedes ajustar este valor según tus necesidades
                    )
                    tarifa = ET.SubElement(impuesto, "tarifa")
                    tarifa.text = "0.00"  # Puedes ajustar este valor según tus necesidades
                    base_imponible_impuesto = ET.SubElement(impuesto, "baseImponible")
                    base_imponible_impuesto.text = str(sale_detail.subtotal)
                    valor_impuesto = ET.SubElement(impuesto, "valor")
                    valor_impuesto.text = "0.00"

                info_adicional = ET.SubElement(root, "infoAdicional")
                campo_adicional = ET.SubElement(info_adicional, "campoAdicional")
                campo_adicional.text = "hcortez2386@uta.edu.ec"
                campo_adicional.set("nombre", "correo")
                xml_content = ET.tostring(root, encoding="utf-8")

                # Devolver el XML como una respuesta HTTP
                response = HttpResponse(content_type="application/xml")
                response["Content-Disposition"] = f'attachment; filename="venta_{sale_id}.xml"'
                response.write(xml_content)
                return response
            else:
                return HttpResponse("No se encontraron detalles de venta para el ID proporcionado")
        except Exception as e:
            print(e)
            return HttpResponse("Error al generar el XML")
