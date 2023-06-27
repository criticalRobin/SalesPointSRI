import os
import django
import sys
import xml.etree.ElementTree as ET
import uuid

django_project_path = 'C:/Users/Matias/OneDrive/Escritorio/Data_Structure/SalesPoint/SalesPoint'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SalesPoint.settings')
sys.path.append(django_project_path)
django.setup()
from SalesPoint.core.erp.models import SaleDetails

try:
    id = input("Ingrese el ID de la compra que desea facturar: ")
    sales = SaleDetails.objects.filter(sale_id=int(id))

    # Verificar si existen detalles de venta para el ID proporcionado
    if sales.exists():
        # Obtener la venta relacionada con los productos
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
        tipo_identificacion_comprador = ET.SubElement(info_factura, "tipoIdentificacionComprador")
        tipo_identificacion_comprador.text = "05"
        razon_social_comprador = ET.SubElement(info_factura, "razonSocialComprador")
        razon_social_comprador.text = f"{sale.client.names} {sale.client.surnames}"
        identificacion_comprador = ET.SubElement(info_factura, "identificacionComprador")
        identificacion_comprador.text = sale.client.dni

        # Agregar más campos adicionales
        id_compra = ET.SubElement(info_factura, "idCompra")
        id_compra.text = str(sale.pk)

        total_sin_impuestos = ET.SubElement(info_factura, "totalSinImpuestos")
        total_sin_impuestos.text = str(sale.subtotal)

        total_descuento = ET.SubElement(info_factura, "totalDescuento")
        total_descuento.text = "0.00"

        total_con_impuestos = ET.SubElement(info_factura, "totalConImpuestos")
        total_impuesto = ET.SubElement(total_con_impuestos, "totalImpuesto")
        codigo = ET.SubElement(total_impuesto, "codigo")
        codigo.text = "2"
        codigo_porcentaje = ET.SubElement(total_impuesto, "codigoPorcentaje")
        codigo_porcentaje.text = "2"
        base_imponible = ET.SubElement(total_impuesto, "baseImponible")
        base_imponible.text = "1.000"
        valor = ET.SubElement(total_impuesto, "valor")
        valor.text = str(sale.iva)

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
            codigo_impuesto.text = "2"  # Puedes ajustar este valor según tus necesidades
            codigo_porcentaje_impuesto = ET.SubElement(impuesto, "codigoPorcentaje")
            codigo_porcentaje_impuesto.text = "2"  # Puedes ajustar este valor según tus necesidades
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

        # Guardar el XML en un archivo
        tree = ET.ElementTree(root)
        tree.write("venta.xml", encoding="utf-8", xml_declaration=True)
        print("Archivo XML generado correctamente.")
    else:
        print("No es un ID de compra válido")
except Exception as e:
    print(f"No es un ID de compra válido: {e}")