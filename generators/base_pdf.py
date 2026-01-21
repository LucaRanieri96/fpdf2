from typing import Literal, List, Dict, Any, Optional, Sequence, Tuple, Callable
from fpdf import FPDF
from fpdf.enums import XPos, YPos, Align, RenderStyle, TableCellFillMode
from fpdf.fonts import FontFace


# 📏 CONFIGURAZIONE FONT STANDARD KOBAK
FONT_CONFIG = {
    'title': {'size': 20, 'height': 24, 'style': 'B'},
    'subtitle': {'size': 15, 'height': 18, 'style': 'B'},
    'heading': {'size': 13, 'height': 16, 'style': 'B'},
    'body': {'size': 11, 'height': 13, 'style': ''},
    'small': {'size': 9, 'height': 11, 'style': 'I'},
}

# 🎨 PALETTE KOBAK
COLORS = {
    'primary': (249, 221, 0),
    'primary_dark': (227, 201, 0),
    'primary_light': (250, 228, 51),
    'secondary': (139, 139, 135),
    'secondary_dark': (76, 75, 72),
    'secondary_light': (204, 204, 199),
    'chip_gray': (119, 119, 119),
    'chip_gray_light': (240, 240, 240),
    'bg_light': (246, 246, 246),
    'bg_white': (255, 255, 255),
    'text_dark': (37, 36, 32),
    'text_light': (180, 180, 176),
    'text_white': (255, 255, 255),
    'status_pending': (245, 158, 11),
    'status_accepted': (16, 185, 129),
    'status_rejected': (239, 68, 68),
}


class KobakPDF(FPDF):
    """
    Libreria di componenti standard per PDF Kobak.

    Ogni metodo rappresenta un "mattoncino" riutilizzabile.
    Tutti i PDF Kobak usano gli stessi componenti per coerenza.
    """

    def __init__(
        self,
        font='Helvetica',
        company_name='KOBAK S.r.l.',
        orientation: Literal['P', 'L'] = 'P',
        format='A4',
        logo_path: Optional[str] = None,
        company_info: Optional[Sequence[str]] = None,
    ):
        super().__init__(orientation=orientation, unit='mm', format=format)
        self.font_family = font
        self.company_name = company_name
        self.logo_path = logo_path
        self.company_info_lines = list(company_info) if company_info else []

        self.set_margins(left=20, top=20, right=20)
        self.set_auto_page_break(auto=True, margin=15)

        self.set_title(f"Documento {company_name}")
        self.set_author(company_name)
        self.footer_note = "SERVIZIO EFFETTUATO IN CONFORMITA' CON LA UNI EN 16194"

    @property
    def content_width(self) -> float:
        return self.w - self.l_margin - self.r_margin

    def header(self):
        """Header con logo e informazioni aziendali al centro"""
        header_height = 32
        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, self.w, header_height, style='F')

        logo_width = 50
        logo_x = (self.w - logo_width) / 2
        logo_y = 6

        if self.logo_path:
            try:
                self.image(self.logo_path, x=logo_x, y=logo_y, w=logo_width, h=15)
            except Exception:
                self._draw_logo_placeholder(logo_x, logo_y, logo_width)
        else:
            self._draw_logo_placeholder(logo_x, logo_y, logo_width)

        if self.company_info_lines:
            self.set_font(self.font_family, '', FONT_CONFIG['small']['size'])
            self.set_text_color(*COLORS['secondary_dark'])
            self.set_xy(self.l_margin, logo_y + 17)
            info_text = " - ".join(self.company_info_lines)
            self.cell(self.content_width, 4.5, text=info_text, align=Align.C)

        self.set_draw_color(*COLORS['secondary_light'])
        self.set_line_width(0.3)
        self.line(self.l_margin, header_height, self.w - self.r_margin, header_height)
        self.set_y(header_height + 3)

    def footer(self):
        """Footer standard con numero pagina"""
        self.set_y(-18)
        self.set_font(self.font_family, '', FONT_CONFIG['small']['size'])
        self.set_text_color(*COLORS['secondary_dark'])
        left_width = self.content_width * 0.7
        right_width = self.content_width - left_width
        self.set_x(self.l_margin)
        self.cell(left_width, FONT_CONFIG['small']['height'], text=self.footer_note, align=Align.C)
        self.cell(right_width, FONT_CONFIG['small']['height'], text=f"Pagina {self.page_no()} di {{nb}}", align=Align.R)

    def add_text(self, text, style='body', color='text_dark', align=Align.L, ln=True):
        """Aggiungi testo con stile predefinito"""
        config = FONT_CONFIG[style]
        self.set_font(self.font_family, config['style'], config['size'])
        self.set_text_color(*COLORS[color])

        if len(text) > 100:
            self.multi_cell(0, config['height'], text, align=align)
        else:
            self.cell(
                0, config['height'], text=text,
                new_x=XPos.LEFT if ln else XPos.RIGHT,
                new_y=YPos.NEXT if ln else YPos.TOP,
                align=align
            )

    def add_paragraph(self, text, align=Align.J):
        """Aggiungi paragrafo con testo a capo automatico"""
        self.set_font(self.font_family, FONT_CONFIG['body']['style'], FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.multi_cell(0, FONT_CONFIG['body']['height'], text, align=align)
        self.ln(2)

    def add_title(self, text):
        """Aggiungi titolo con bordo"""
        self.set_font(self.font_family, FONT_CONFIG['title']['style'], FONT_CONFIG['title']['size'])
        self.set_text_color(*COLORS['primary_dark'])

        width = self.get_string_width(text) + 6
        self.set_x((self.w - width) / 2)

        self.cell(
            width, FONT_CONFIG['title']['height'], text,
            border=1, align=Align.C, fill=True,
            new_x=XPos.LEFT, new_y=YPos.NEXT
        )
        self.ln(5)

    def add_heading(self, text):
        """Aggiungi intestazione sezione"""
        self.set_font(self.font_family, FONT_CONFIG['heading']['style'], FONT_CONFIG['heading']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.cell(
            0, FONT_CONFIG['heading']['height'], text,
            new_x=XPos.LEFT, new_y=YPos.NEXT
        )
        self.ln(2)

    def add_table(self, data, headers=None, col_widths=None, style='styled'):
        """Aggiungi tabella stilizzata"""
        if style == 'styled':
            headings_style = FontFace(
                emphasis="BOLD",
                color=(255, 255, 255),
                fill_color=COLORS['primary']
            )

            with self.table(
                borders_layout="MINIMAL",
                cell_fill_color=COLORS['bg_light'],
                col_widths=col_widths,
                headings_style=headings_style,
                line_height=6,
                width=160,
            ) as table:
                if headers:
                    row = table.row()
                    for header in headers:
                        row.cell(header)

                for data_row in data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(str(datum))
        else:
            with self.table() as table:
                if headers:
                    row = table.row()
                    for header in headers:
                        row.cell(header)

                for data_row in data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(str(datum))

    def add_columns(self, texts, ncols=2, gutter=10, text_align=Align.J):
        """Aggiungi testo su più colonne"""
        with self.text_columns(
            ncols=ncols,
            gutter=gutter,
            text_align=text_align,
            line_height=1.2
        ) as cols:
            for text in texts:
                self.set_font(self.font_family, size=FONT_CONFIG['body']['size'])
                cols.write(text)

    def add_clickable_link(self, text, url=None, page=None):
        """Aggiungi link cliccabile"""
        if url:
            self.set_font(self.font_family, 'U', FONT_CONFIG['body']['size'])
            self.set_text_color(0, 0, 255)
            self.write(FONT_CONFIG['body']['height'], text, url)

        elif page:
            link = super().add_link(page=page)
            self.set_font(self.font_family, 'U', FONT_CONFIG['body']['size'])
            self.set_text_color(0, 0, 255)
            self.write(FONT_CONFIG['body']['height'], text, link)

        self.set_text_color(*COLORS['text_dark'])
        self.set_font(style='')

    def add_status_badge(self, status_text, status_type='pending'):
        """Aggiungi badge di stato colorato"""
        status_colors = {
            'pending': COLORS['status_pending'],
            'accepted': COLORS['status_accepted'],
            'rejected': COLORS['status_rejected'],
        }

        color = status_colors.get(status_type, COLORS['secondary'])

        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font(self.font_family, 'B', FONT_CONFIG['small']['size'])

        self.cell(
            50, 8, text=f" {status_text} ",
            border=1, align=Align.C, fill=True,
            new_x=XPos.LEFT, new_y=YPos.NEXT
        )

        self.set_text_color(*COLORS['text_dark'])

    def add_spacing(self, height=5):
        """Aggiungi spazio verticale"""
        self.ln(height)

    def add_section(self, title, content, content_type='list'):
        """Aggiungi sezione con titolo e contenuto"""
        self.add_heading(title)

        if content_type == 'list':
            for item in content:
                self.add_text(f"- {item}", style='body')
        elif content_type == 'paragraph':
            self.add_paragraph(content)
        elif content_type == 'columns':
            self.add_columns(content)

        self.add_spacing()

    def add_line(self, color='primary', width=0.5):
        """Aggiungi linea orizzontale"""
        self.set_draw_color(*COLORS[color])
        self.set_line_width(width)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.ln(3)

    # ========================================
    # COMPONENTI STANDARD KOBAK (Mattoncini)
    # ========================================

    def add_document_title(self, title: str):
        """
        Titolo documento standard Kobak.
        Usato per: FATTURA, PREVENTIVO, REPORT, ecc.
        """
        self.set_font(self.font_family, 'B', FONT_CONFIG['title']['size'])
        self.set_text_color(*COLORS['text_white'])

        width = self.w - self.l_margin - self.r_margin
        self.set_fill_color(*COLORS['primary'])
        self.set_draw_color(*COLORS['primary_dark'])
        self.rect(self.l_margin, self.get_y(), width, FONT_CONFIG['title']['height'] + 4, style='DF')

        self.set_x(self.l_margin + 4)
        self.cell(
            width - 8, FONT_CONFIG['title']['height'], title,
            border=0, align=Align.L, fill=False,
            new_x=XPos.LEFT, new_y=YPos.NEXT
        )
        self.ln(3)

    def add_document_info(self, number: str, date: str, label_prefix: str = "Documento"):
        """
        Box informazioni documento (numero e data).
        Layout standard Kobak: colonna sinistra.
        """
        gutter = 6
        col_width = (self.w - self.l_margin - self.r_margin - gutter) / 2
        box_y = self.get_y()
        lines = 2
        box_height = lines * 7 + 6

        self.set_fill_color(*COLORS['bg_light'])
        self.set_draw_color(*COLORS['secondary_light'])
        self.rect(self.l_margin, box_y, col_width, box_height, style='DF')

        self.set_xy(self.l_margin + 4, box_y + 3)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['secondary_dark'])
        self.cell(col_width - 8, 6, text=label_prefix.upper(), new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_x(self.l_margin + 4)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.cell(25, 6, text="Numero:", new_x=XPos.RIGHT)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.cell(col_width - 37, 6, text=number, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_x(self.l_margin + 4)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.cell(25, 6, text="Data:", new_x=XPos.RIGHT)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.cell(col_width - 37, 6, text=date, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_y(box_y + box_height)
        return box_y, box_height, col_width, gutter

    def add_client_info(self, client_name: str, vat_number: str, address: str = None, anchor_y: float = None, col_width: float = None, gutter: float = 6):
        """
        Box informazioni cliente standard Kobak.
        Layout standard: colonna destra.
        """
        col_width = col_width or (self.w - self.l_margin - self.r_margin - gutter) / 2
        box_y = anchor_y if anchor_y is not None else self.get_y()
        x_start = self.l_margin + col_width + gutter

        lines = 2 + (1 if address else 0)
        box_height = lines * 7 + 6

        self.set_fill_color(*COLORS['bg_light'])
        self.set_draw_color(*COLORS['secondary_light'])
        self.rect(x_start, box_y, col_width, box_height, style='DF')

        self.set_xy(x_start + 4, box_y + 3)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['secondary_dark'])
        self.cell(col_width - 8, 6, text="CLIENTE", new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_x(x_start + 4)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.cell(28, 6, text="Ragione:", new_x=XPos.RIGHT)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.cell(col_width - 40, 6, text=client_name, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_x(x_start + 4)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.cell(28, 6, text="P.IVA:", new_x=XPos.RIGHT)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.cell(col_width - 40, 6, text=vat_number, new_x=XPos.LEFT, new_y=YPos.NEXT)

        if address:
            self.set_x(x_start + 4)
            self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
            self.cell(28, 6, text="Indirizzo:", new_x=XPos.RIGHT)
            
            self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
            self.cell(col_width - 40, 6, text=address, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_y(box_y + box_height)
        return box_height

    def add_items_table(self, items: List[Dict[str, Any]], headers: List[str] = None):
        """
        Tabella articoli standard Kobak.
        
        items: lista di dict con keys ['description', 'qty', 'unit_price', 'total']
        """
        if headers is None:
            headers = ['Descrizione', 'Q.ta', 'Prezzo Unit.', 'Importo']

        headings_style = FontFace(
            emphasis="BOLD",
            color=COLORS['text_white'],
            fill_color=COLORS['primary_dark']
        )

        body_style = FontFace(color=COLORS['text_dark'])
        zebra_style = FontFace(color=COLORS['text_dark'], fill_color=COLORS['bg_light'])

        products = [
            [item.get('description', ''),
             str(item.get('qty', '')),
             item.get('unit_price', ''),
             item.get('total', '')]
            for item in items
        ]

        table_width = self.w - self.l_margin - self.r_margin
        col_widths = [table_width * 0.54, table_width * 0.12, table_width * 0.16, table_width * 0.18]

        with self.table(
            borders_layout="ALL",
            cell_fill_color=COLORS['bg_white'],
            col_widths=col_widths,
            headings_style=headings_style,
            line_height=7,
            width=table_width,
        ) as table:
            row = table.row()
            for header in headers:
                row.cell(header)

            for idx, data_row in enumerate(products):
                row_style = zebra_style if idx % 2 == 0 else body_style
                row = table.row(style=row_style)
                for datum in data_row:
                    row.cell(str(datum))

    def add_totals_section(self, subtotal: str, vat: str, total: str, vat_rate: str = "22%"):
        """
        Sezione totali standard Kobak.
        Sempre allineata a destra, sempre con lo stesso layout.
        """
        self.ln(2)

        box_width = 80
        box_height = 27
        x_start = self.w - self.r_margin - box_width
        y_start = self.get_y()

        self.set_fill_color(*COLORS['primary_light'])
        self.set_draw_color(*COLORS['primary_dark'])
        self.rect(x_start, y_start, box_width, box_height, style='DF')

        self.set_xy(x_start + 5, y_start + 4)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.cell(40, 6, text=f"Subtotale", new_x=XPos.RIGHT)
        self.cell(35, 6, text=subtotal, align=Align.R, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_x(x_start + 5)
        self.cell(40, 6, text=f"IVA ({vat_rate})", new_x=XPos.RIGHT)
        self.cell(35, 6, text=vat, align=Align.R, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_x(x_start + 5)
        self.set_font(self.font_family, 'B', FONT_CONFIG['heading']['size'])
        self.set_text_color(*COLORS['secondary_dark'])
        self.cell(40, 7, text="TOTALE", new_x=XPos.RIGHT)
        self.set_text_color(*COLORS['text_dark'])
        self.cell(35, 7, text=total, align=Align.R, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_y(y_start + box_height)

    def add_notes_section(self, notes: str):
        """
        Sezione note finali standard Kobak.
        """
        if not notes:
            return
        self.ln(6)
        box_width = self.w - self.l_margin - self.r_margin
        box_y = self.get_y()
        estimated_height = max(24, (len(notes) // 70 + 1) * 5 + 14)

        self.set_fill_color(*COLORS['bg_light'])
        self.set_draw_color(*COLORS['secondary_light'])
        self.rect(self.l_margin, box_y, box_width, estimated_height, style='DF')

        self.set_xy(self.l_margin + 4, box_y + 4)
        self.set_font(self.font_family, 'B', FONT_CONFIG['heading']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.cell(box_width - 8, 6, text="Note", new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.set_x(self.l_margin + 4)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['secondary_dark'])
        self.multi_cell(box_width - 8, 5, text=notes)

        self.set_y(max(self.get_y(), box_y + estimated_height))

    def add_validity_info(self, valid_until: str, anchor_y: float = None, col_width: float = None, gutter: float = 6):
        """
        Informazioni validità (per preventivi).
        """
        col_width = col_width or (self.w - self.l_margin - self.r_margin - gutter) / 2
        box_y = anchor_y if anchor_y is not None else self.get_y()
        x_start = self.l_margin + col_width + gutter
        box_height = 12

        self.set_fill_color(*COLORS['primary_light'])
        self.set_draw_color(*COLORS['primary_dark'])
        self.rect(x_start, box_y, col_width, box_height, style='DF')

        self.set_xy(x_start + 4, box_y + 3)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['secondary_dark'])
        self.cell(col_width - 8, 5, text=f"Valido fino al {valid_until}")

        self.set_y(box_y + box_height)
        return box_height

    def add_section_heading(self, title: str):
        """
        Intestazione sezione standard Kobak.
        """
        self.set_font(self.font_family, 'B', FONT_CONFIG['heading']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.cell(0, FONT_CONFIG['heading']['height'], text=title,
                 new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.set_draw_color(*COLORS['secondary_light'])
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def _draw_logo_placeholder(self, x: float, y: float, width: float):
        height = 15
        self.set_draw_color(*COLORS['secondary_light'])
        self.rect(x, y, width, height)
        self.set_font(self.font_family, 'I', FONT_CONFIG['small']['size'])
        self.set_text_color(*COLORS['text_light'])
        self.set_xy(x, y + height / 2 - 3)
        self.cell(width, 6, text='LOGO', align=Align.C)

    def add_section_chip(self, title: str, variant: Literal['gold', 'gray'] = 'gold'):
        colors = {
            'gold': (COLORS['primary'], COLORS['text_dark']),
            'gray': (COLORS['chip_gray'], COLORS['text_white']),
        }
        fill_color, text_color = colors.get(variant, colors['gold'])
        chip_height = 9
        chip_y = self.get_y()
        self.set_fill_color(*fill_color)
        self.set_text_color(*text_color)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])

        try:
            self.rounded_rect(self.l_margin, chip_y, self.content_width, chip_height + 4, 2.5, style='F')
        except AttributeError:
            self.rect(self.l_margin, chip_y, self.content_width, chip_height + 4, style='F')

        self.set_xy(self.l_margin + 3, chip_y + 1.5)
        self.cell(self.content_width - 6, chip_height, text=title.upper(), align=Align.L)
        self.ln(chip_height + 5)

    def add_offer_section_title(self, title: str, variant: Literal['gold', 'gray'] = 'gold'):
        """Header giallo/gray stile offerta"""
        self.add_section_chip(title=title, variant=variant)

    def add_labeled_line(self, label: str, value: str):
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.set_text_color(*COLORS['text_dark'])
        self.cell(0, 5, text=f"{label}: {value}", new_x=XPos.LEFT, new_y=YPos.NEXT)

    def _measure_text_height(self, text: str, width: float, line_height: float) -> float:
        if not text:
            return line_height
        lines = self.multi_cell(width, line_height, text, dry_run=True, output='LINES')
        return max(line_height, len(lines) * line_height)

    def add_info_card(
        self,
        title: Optional[str],
        rows: List[Tuple[str, str]],
        width: Optional[float] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        variant: Literal['gold', 'gray'] = 'gold',
        label_width: float = 32,
    ) -> float:
        width = width or self.content_width
        x = x if x is not None else self.l_margin
        y = y if y is not None else self.get_y()
        padding = 4.5
        header_height = 9 if title else 0
        line_height = FONT_CONFIG['body']['height']
        text_width = width - (padding * 2 + label_width)

        card_height = header_height + padding
        for idx, (label, value) in enumerate(rows):
            text_value = value or '-'
            text_area_width = text_width if label else width - padding * 2
            card_height += self._measure_text_height(text_value, text_area_width, line_height)
            if idx < len(rows) - 1:
                card_height += 0.8
        card_height += padding

        self.set_draw_color(*COLORS['secondary_light'])
        self.set_fill_color(*COLORS['bg_white'])
        try:
            self.rounded_rect(x, y, width, card_height, 2.4, style='DF')
        except AttributeError:
            self.rect(x, y, width, card_height, style='DF')

        if title:
            chip_colors = {
                'gold': (COLORS['primary'], COLORS['text_dark']),
                'gray': (COLORS['chip_gray'], COLORS['text_white'])
            }
            fill_color, text_color = chip_colors.get(variant, chip_colors['gold'])
            self.set_fill_color(*fill_color)
            try:
                self.rounded_rect(x, y, width, header_height + 2.4, 2.4, style='F')
            except AttributeError:
                self.rect(x, y, width, header_height, style='F')
            self.set_xy(x + padding, y + 2)
            self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
            self.set_text_color(*text_color)
            self.cell(width - padding * 2, header_height - 2, text=title.upper())

        cursor_y = y + header_height + padding
        for idx, (label, value) in enumerate(rows):
            text_value = value or '-'
            self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
            self.set_text_color(*COLORS['secondary_dark'])

            if label:
                row_height = self._measure_text_height(text_value, text_width, line_height)
                self.set_xy(x + padding, cursor_y)
                self.cell(label_width, line_height, text=f"{label}:", align=Align.L)

                self.set_xy(x + padding + label_width, cursor_y)
                self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
                self.set_text_color(*COLORS['text_dark'])
                self.multi_cell(text_width, line_height, text=text_value)
            else:
                row_height = self._measure_text_height(text_value, width - padding * 2, line_height)
                self.set_xy(x + padding, cursor_y)
                self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
                self.set_text_color(*COLORS['text_dark'])
                self.multi_cell(width - padding * 2, line_height, text=text_value)

            cursor_y += row_height
            if idx < len(rows) - 1:
                self.set_draw_color(*COLORS['secondary_light'])
                self.line(x + padding, cursor_y, x + width - padding, cursor_y)
                cursor_y += 0.8

        self.set_y(max(self.get_y(), y + card_height))
        return card_height

    def add_details_table(self, rows: List[Dict[str, str]]):
        headers = ['DESCRIZIONE', 'QUANTITA', 'UNITA', 'PREZZO UNIT.', 'PREZZO TOTALE']
        table_width = self.content_width
        col_widths = [table_width * 0.4, table_width * 0.12, table_width * 0.12, table_width * 0.18, table_width * 0.18]

        headings_style = FontFace(emphasis='BOLD', color=COLORS['text_dark'], fill_color=COLORS['chip_gray_light'])
        zebra_even = FontFace(color=COLORS['text_dark'], fill_color=COLORS['bg_light'])
        zebra_odd = FontFace(color=COLORS['text_dark'], fill_color=COLORS['bg_white'])

        self.set_x(self.l_margin)
        with self.table(
            borders_layout='ALL',
            cell_fill_color=COLORS['bg_white'],
            col_widths=col_widths,
            headings_style=headings_style,
            line_height=6,
            width=table_width,
        ) as table:
            header_row = table.row()
            for header in headers:
                header_row.cell(header)

            for idx, item in enumerate(rows):
                row_style = zebra_even if idx % 2 == 0 else zebra_odd
                row = table.row(style=row_style)
                row.cell(item.get('description', ''))
                row.cell(str(item.get('quantity', '')))
                row.cell(item.get('unit', ''))
                row.cell(item.get('unit_price', ''))
                row.cell(item.get('total_price', ''))

    def add_totals_list(self, totals: List[Tuple[str, str]], highlight_last: bool = True):
        row_height = 8
        for idx, (label, value) in enumerate(totals):
            is_last = highlight_last and idx == len(totals) - 1
            fill = COLORS['primary_light'] if is_last else COLORS['bg_light']
            text_color = COLORS['text_dark']
            self.set_fill_color(*fill)
            self.set_text_color(*text_color)
            self.set_font(self.font_family, 'B' if is_last else '', FONT_CONFIG['body']['size'])

            self.set_x(self.l_margin)
            self.cell(self.content_width * 0.65, row_height, text=label.upper(), align=Align.L, fill=True, border=1)
            self.cell(self.content_width * 0.35, row_height, text=value, align=Align.R, fill=True, border=1, new_x=XPos.LEFT, new_y=YPos.NEXT)

        self.ln(2)

    def add_signature_blocks(self, blocks: List[Dict[str, str]], gutter: float = 6):
        if not blocks:
            return
        column_width = (self.content_width - gutter * (len(blocks) - 1)) / len(blocks)
        start_y = self.get_y()
        heights = []

        for idx, block in enumerate(blocks):
            x = self.l_margin + idx * (column_width + gutter)
            heights.append(self._render_signature_block(block, x, start_y, column_width))

        self.set_y(start_y + max(heights) + 4)

    def _render_signature_block(self, block: Dict[str, str], x: float, y: float, width: float) -> float:
        padding = 4
        line_height = FONT_CONFIG['body']['height']
        title = block.get('title', '')
        instructions = block.get('instructions', '')

        height = 50
        self.set_fill_color(*COLORS['bg_white'])
        self.set_draw_color(*COLORS['secondary_light'])
        self.rect(x, y, width, height, style='DF')

        self.set_xy(x + padding, y + padding)
        self.set_font(self.font_family, 'B', FONT_CONFIG['body']['size'])
        self.cell(width - padding * 2, line_height, text=title.upper())

        self.set_xy(x + padding, y + padding + line_height + 2)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.multi_cell(width - padding * 2, line_height - 1, instructions)

        self.set_xy(x + padding, y + height - 14)
        self.set_font(self.font_family, '', FONT_CONFIG['body']['size'])
        self.cell(width * 0.5, line_height, text='IL CLIENTE')
        self.set_xy(x + padding, y + height - 8)
        self.cell(width - padding * 2, line_height, text='(Timbro e Firma)', align=Align.L)
        return height

    def add_contract_terms(self, clauses: List[str]):
        self.set_font(self.font_family, '', FONT_CONFIG['small']['size'])
        self.set_text_color(*COLORS['text_dark'])
        for idx, clause in enumerate(clauses, start=1):
            self.multi_cell(0, FONT_CONFIG['small']['height'], text=f"{idx}. {clause}")
            self.ln(1)

    # ==================== COMPONENTI AGGIUNTIVI PER CONTRATTI ====================
    
    def rounded_rect(self, x: float, y: float, w: float, h: float, r: float, style: str = ''):
        """
        Disegna un rettangolo con angoli arrotondati.
        
        Args:
            x: Coordinata X (angolo alto-sinistra)
            y: Coordinata Y (angolo alto-sinistra)
            w: Larghezza
            h: Altezza
            r: Raggio degli angoli arrotondati
            style: 'D' draw, 'F' fill, 'DF' draw+fill
        """
        render_style = RenderStyle.coerce(style) if style else RenderStyle.D
        self.rect(x, y, w, h, style=render_style, round_corners=True, corner_radius=r)
    
    def add_label_value_line(self, label: str, value: str, 
                            label_width: float = None,
                            line_height: float = 4,
                            label_style: str = 'B',
                            value_style: str = '',
                            font_size: int = 7):
        """
        Riga con formato "Label: Value".
        
        Args:
            label: Testo label (grassetto)
            value: Testo valore
            label_width: Larghezza area label (default: 40)
            line_height: Altezza riga
            label_style: Stile font label
            value_style: Stile font valore
            font_size: Dimensione font
        """
        page_width = self.content_width
        lbl_width = label_width if label_width is not None else 40
        
        # Reset posizione X
        self.set_x(self.l_margin)
        
        # Label
        self.set_font(self.font_family, label_style, font_size)
        self.cell(lbl_width, line_height, label, new_x=XPos.RIGHT)
        
        # Value
        self.set_font(self.font_family, value_style, font_size)
        self.cell(page_width - lbl_width, line_height, value, new_x=XPos.LEFT, new_y=YPos.NEXT)
    
    def add_two_columns_with_callbacks(self, left_fn: Callable, right_fn: Callable,
                                      col_ratio: float = 0.5, gutter: float = 3,
                                      return_to_max_y: bool = True):
        """
        Layout a due colonne con funzioni callback per il contenuto.
        
        Args:
            left_fn: Funzione che genera contenuto colonna sinistra
            right_fn: Funzione che genera contenuto colonna destra
            col_ratio: Rapporto larghezza sinistra/totale (0-1)
            gutter: Spazio tra colonne
            return_to_max_y: Se True, posiziona cursore dopo colonna più lunga
        """
        page_width = self.content_width
        left_width = page_width * col_ratio - gutter / 2
        right_width = page_width * (1 - col_ratio) - gutter / 2
        
        y_start = self.get_y()
        x_left = self.l_margin
        x_right = self.l_margin + left_width + gutter
        
        # Colonna sinistra
        self.set_xy(x_left, y_start)
        left_fn()
        left_end_y = self.get_y()
        
        # Colonna destra
        self.set_xy(x_right, y_start)
        right_fn()
        right_end_y = self.get_y()
        
        # Posiziona cursore
        if return_to_max_y:
            self.set_y(max(left_end_y, right_end_y))
    
    def add_columns_with_headers(self, 
                                left_header: str, left_fn: Callable,
                                right_header: str, right_fn: Callable,
                                col_ratio: float = 0.5, gutter: float = 3,
                                left_header_bg: str = 'primary',
                                right_header_bg: str = 'chip_gray'):
        """
        Due colonne con header separati usando callback.
        
        Args:
            left_header: Testo header sinistra
            left_fn: Funzione contenuto sinistra
            right_header: Testo header destra
            right_fn: Funzione contenuto destra
            col_ratio: Rapporto colonne
            gutter: Spazio tra colonne
            left_header_bg: Nome colore header sinistra (da COLORS)
            right_header_bg: Nome colore header destra (da COLORS)
        """
        page_width = self.content_width
        left_width = page_width * col_ratio - gutter / 2
        right_width = page_width * (1 - col_ratio) - gutter / 2
        
        y_start = self.get_y()
        x_left = self.l_margin
        x_right = self.l_margin + left_width + gutter
        
        # Colonna sinistra
        self.set_xy(x_left, y_start)
        if left_header:
            # Header sinistra
            bg_color = COLORS.get(left_header_bg, COLORS['primary'])
            self.set_fill_color(*bg_color)
            self.set_text_color(*COLORS['text_dark'])
            self.set_font(self.font_family, 'B', 9)
            
            y_pos = self.get_y()
            self.rounded_rect(x_left, y_pos, left_width, 7, 2, style='F')
            self.set_xy(x_left, y_pos)
            self.cell(left_width, 7, left_header, border=0, align=Align.C, fill=False, 
                     new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.set_x(x_left)
            self.ln(2)
            
            self.set_text_color(*COLORS['text_dark'])
            self.set_fill_color(*COLORS['bg_white'])
        
        # IMPORTANTE: Assicura che left_fn inizi dalla X corretta
        self.set_x(x_left)
        left_fn()
        left_end_y = self.get_y()
        
        # Colonna destra
        self.set_xy(x_right, y_start)
        if right_header:
            # Header destra
            bg_color = COLORS.get(right_header_bg, COLORS['chip_gray'])
            self.set_fill_color(*bg_color)
            self.set_text_color(*COLORS['text_white'])
            self.set_font(self.font_family, 'B', 9)
            
            y_pos = self.get_y()
            self.rounded_rect(x_right, y_pos, right_width, 7, 2, style='F')
            self.set_xy(x_right, y_pos)
            self.cell(right_width, 7, right_header, border=0, align=Align.C, fill=False, 
                     new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.set_x(x_right)
            self.ln(2)
            
            self.set_text_color(*COLORS['text_dark'])
            self.set_fill_color(*COLORS['bg_white'])
        
        # IMPORTANTE: Assicura che right_fn inizi dalla X corretta
        self.set_x(x_right)
        right_fn()
        right_end_y = self.get_y()
        
        # Posiziona cursore dopo la colonna più lunga
        self.set_y(max(left_end_y, right_end_y))
    
    def add_checkbox(self, x: float = None, y: float = None, 
                    size: float = 4, checked: bool = False,
                    corner_radius: float = 0.5):
        """
        Disegna un singolo checkbox.
        
        Args:
            x: Coordinata X (None = posizione corrente)
            y: Coordinata Y (None = posizione corrente)
            size: Dimensione checkbox
            checked: Se True, disegna una X
            corner_radius: Raggio angoli
        """
        x_pos = x if x is not None else self.get_x()
        y_pos = y if y is not None else self.get_y()
        
        self.set_draw_color(0, 0, 0)
        self.rounded_rect(x_pos, y_pos, size, size, corner_radius, style='D')
        
        if checked:
            self.set_xy(x_pos, y_pos)
            self.set_font(self.font_family, 'B', 7)
            self.cell(size, size, "X", align=Align.C)
    
    def add_checkbox_row(self, items: list, spacing: float = 10, 
                        checkbox_size: float = 4, font_size: int = 7):
        """
        Riga orizzontale di checkbox con label.
        
        Args:
            items: Lista di label (str) o tuple (label, checked)
            spacing: Spazio tra checkbox
            checkbox_size: Dimensione checkbox
            font_size: Dimensione font label
        """
        for i, item in enumerate(items):
            # Parse item
            if isinstance(item, tuple):
                label, checked = item
            else:
                label, checked = item, False
            
            # Checkbox
            self.add_checkbox(size=checkbox_size, checked=checked)
            self.cell(checkbox_size + 2, checkbox_size, "", new_x=XPos.RIGHT)
            
            # Label
            self.set_font(self.font_family, '', font_size)
            self.cell(0, checkbox_size, label, 
                     new_x=XPos.RIGHT if i < len(items) - 1 else XPos.LEFT)
            
            # Spacing
            if i < len(items) - 1:
                self.cell(spacing, checkbox_size, "", new_x=XPos.RIGHT)
        
        self.ln(6)
    
    def add_table_row_with_fill(self, cells: list, widths: list, height: float = 5,
                                fill: bool = False, fill_color: Tuple[int, int, int] = None,
                                border: int = 0, font_size: int = 7, font_style: str = '',
                                aligns: list = None, corner_radius: float = 0,
                                multiline: bool = False):
        """
        Riga di tabella con celle personalizzabili e background arrotondato.
        
        Args:
            cells: Lista di contenuti celle
            widths: Lista di larghezze celle (percentuali 0-1 o assolute)
            height: Altezza riga
            fill: Se True, usa colore di riempimento
            fill_color: Tupla RGB per fill (default: bg_light)
            border: Bordi celle (0=no, 1=si)
            font_size: Dimensione font
            font_style: Stile font
            aligns: Lista allineamenti per cella ('L', 'C', 'R')
            corner_radius: Raggio angoli se fill=True
            multiline: Se True, usa multi_cell per celle lunghe (auto-height)
        """
        page_width = self.content_width
        
        # Normalizza widths
        normalized_widths = []
        for w in widths:
            if 0 < w <= 1:
                normalized_widths.append(w * page_width)
            else:
                normalized_widths.append(w)
        
        # Setup aligns
        if aligns is None:
            aligns = ['L'] * len(cells)
        
        # Reset X
        self.set_x(self.l_margin)
        self.set_font(self.font_family, font_style, font_size)
        
        # FASE 1: Calcola altezza massima necessaria
        y_start = self.get_y()
        max_height = height
        
        for i, (cell, width) in enumerate(zip(cells, normalized_widths)):
            cell_text = str(cell)
            # Prima colonna: controlla se serve wrapping
            if i == 0 and len(cell_text) > 45:
                # Calcola altezza necessaria senza disegnare
                lines = len(cell_text) // 40 + 1
                estimated_height = lines * height * 0.8
                max_height = max(max_height, estimated_height)
        
        # FASE 2: Disegna il fill con l'altezza corretta
        if fill:
            color = fill_color if fill_color else COLORS.get('bg_light', (246, 246, 246))
            self.set_fill_color(*color)
            
            if corner_radius > 0:
                self.rounded_rect(self.l_margin, y_start, page_width, max_height, corner_radius, style='F')
            else:
                self.rect(self.l_margin, y_start, page_width, max_height, style='F')
        
        # FASE 3: Disegna il testo SOPRA il fill
        self.set_xy(self.l_margin, y_start)
        
        for i, (cell, width, align) in enumerate(zip(cells, normalized_widths, aligns)):
            cell_text = str(cell)
            x_pos = self.get_x()
            
            # Prima colonna: controlla se serve wrapping
            if i == 0 and len(cell_text) > 45:
                # Disegna prima il bordo con l'altezza completa
                if border:
                    self.rect(x_pos, y_start, width, max_height)
                
                # Poi usa multi_cell per wrapping SENZA bordo
                self.multi_cell(width, height * 0.8, cell_text, border=0, align=align)
                # Torna all'inizio della riga e vai alla prossima colonna
                self.set_xy(x_pos + width, y_start)
            else:
                # Altre colonne: cell standard
                self.cell(width, max_height, cell_text, border=border, align=align,
                         fill=False,
                         new_x=XPos.RIGHT, new_y=YPos.TOP)
        
        # Posiziona dopo la riga (alla max_height)
        self.set_xy(self.l_margin, y_start + max_height)
    
    def reset_x(self):
        """Reset X al margine sinistro"""
        self.set_x(self.l_margin)
    
    def add_info_grid(self, rows: List[Tuple[str, str]], 
                      label_width: float = 28, 
                      line_height: float = 4,
                      font_size: int = 7,
                      max_value_width: float = None):
        """
        Griglia info label/valore (pattern comune nei contratti).
        
        Args:
            rows: Lista di tuple (label, value)
            label_width: Larghezza colonna label
            line_height: Altezza riga
            font_size: Dimensione font
            max_value_width: Larghezza massima per valore (auto se None)
        """
        for label, value in rows:
            # Salva posizione X iniziale (importante per colonne)
            x_start = self.get_x()
            
            # Label in grassetto
            self.set_font(self.font_family, 'B', font_size)
            self.cell(label_width, line_height, label, new_x=XPos.RIGHT)
            
            # Value: calcola larghezza disponibile
            self.set_font(self.font_family, '', font_size)
            
            if max_value_width is not None:
                # Usa larghezza esplicita se fornita (modalità colonne)
                value_width = max_value_width
            else:
                # Calcola automaticamente fino al margine destro
                current_x = self.get_x()
                value_width = (self.w - self.r_margin) - current_x
            
            # Disegna valore
            self.cell(value_width, line_height, value, 
                     new_x=XPos.LEFT, new_y=YPos.NEXT)
            
            # IMPORTANTE: Reset X alla posizione iniziale per la prossima riga
            # Questo garantisce che tutte le righe partano dalla stessa X
            self.set_x(x_start)
    
    def add_form_checkboxes(self, options: List[str], 
                           checked_indices: List[int] = None,
                           checkbox_size: float = 4,
                           spacing: float = 1,
                           font_size: int = 7):
        """
        Lista checkbox verticale con label (per form).
        
        Args:
            options: Lista di opzioni (testi)
            checked_indices: Indici delle checkbox da marcare come selezionate
            checkbox_size: Dimensione checkbox
            spacing: Spaziatura tra checkbox
            font_size: Dimensione font
        """
        checked_indices = checked_indices or []
        for i, option in enumerate(options):
            y_start = self.get_y()
            x_start = self.get_x()
            self.add_checkbox(
                x=x_start, 
                y=y_start, 
                size=checkbox_size,
                checked=(i in checked_indices)
            )
            self.set_xy(x_start + checkbox_size + 2, y_start)
            self.set_font(self.font_family, '', font_size)
            available_width = (self.w - self.r_margin) - self.get_x()
            self.cell(available_width, checkbox_size, option, new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.ln(spacing)
    
    def add_two_column_info_boxes(self, 
                                  left_header: str, left_rows: List[Tuple[str, str]],
                                  right_header: str, right_rows: List[Tuple[str, str]],
                                  left_header_bg: str = 'primary',
                                  right_header_bg: str = 'chip_gray',
                                  col_ratio: float = 0.5,
                                  gutter: float = 3,
                                  label_width: float = 28):
        """
        Due box info affiancati con header colorati (es: cliente + sede).
        
        Args:
            left_header: Titolo colonna sinistra
            left_rows: Righe info sinistra (lista tuple label/valore)
            right_header: Titolo colonna destra
            right_rows: Righe info destra (lista tuple label/valore)
            left_header_bg: Colore background header sinistro
            right_header_bg: Colore background header destro
            col_ratio: Rapporto larghezza colonne
            gutter: Spaziatura tra colonne
            label_width: Larghezza label nelle info grid
        """
        # Calcola larghezze colonne
        page_width = self.content_width
        left_width = page_width * col_ratio - gutter / 2
        right_width = page_width * (1 - col_ratio) - gutter / 2
        
        # Calcola larghezza max per i valori (colonna - label_width)
        left_value_width = left_width - label_width
        right_value_width = right_width - label_width
        
        def left_fn():
            self.add_info_grid(left_rows, label_width=label_width, 
                             max_value_width=left_value_width)
        
        def right_fn():
            self.add_info_grid(right_rows, label_width=label_width,
                             max_value_width=right_value_width)
        
        self.add_columns_with_headers(
            left_header=left_header, left_fn=left_fn,
            right_header=right_header, right_fn=right_fn,
            col_ratio=col_ratio,
            gutter=gutter,
            left_header_bg=left_header_bg,
            right_header_bg=right_header_bg
        )
    
    def add_info_section(self, 
                        rows: List[Tuple[str, str]] = None,
                        header: str = None,
                        header_bg: str = 'primary',
                        label_width: float = 28,
                        two_columns: bool = False,
                        left_rows: List[Tuple[str, str]] = None,
                        right_rows: List[Tuple[str, str]] = None,
                        left_header: str = None,
                        right_header: str = None,
                        left_header_bg: str = 'primary',
                        right_header_bg: str = 'chip_gray',
                        col_ratio: float = 0.5,
                        gutter: float = 3):
        """
        🌟 COMPONENTE UNIVERSALE per sezioni info dinamiche.
        Gestisce automaticamente layout singolo o doppio con header opzionali.
        Passa solo liste di dati, lui fa tutto!
        
        MODALITÀ 1 - Singola colonna semplice:
            pdf.add_info_section(rows=[('Label:', 'Value'), ...])
        
        MODALITÀ 2 - Singola colonna con header:
            pdf.add_info_section(
                header='DATI CLIENTE',
                rows=[('Nome:', 'Mario'), ...],
                header_bg='primary'
            )
        
        MODALITÀ 3 - Due colonne con header:
            pdf.add_info_section(
                two_columns=True,
                left_header='CLIENTE',
                left_rows=[('Nome:', 'Mario'), ...],
                right_header='SEDE',
                right_rows=[('Indirizzo:', 'Via...')],
                left_header_bg='primary',
                right_header_bg='chip_gray'
            )
        
        Args:
            rows: Lista (label, value) per layout singolo
            header: Titolo opzionale per layout singolo
            header_bg: Colore background header singolo
            label_width: Larghezza label nelle griglie
            two_columns: Se True, usa layout a due colonne
            left_rows/right_rows: Liste per colonne separate
            left_header/right_header: Titoli colonne
            left_header_bg/right_header_bg: Colori header
            col_ratio: Rapporto larghezza (default 50/50)
            gutter: Spazio tra colonne
        """
        if two_columns:
            # LAYOUT DUE COLONNE
            if not left_rows and not right_rows:
                raise ValueError("Devi fornire left_rows e/o right_rows per two_columns=True")
            
            self.add_two_column_info_boxes(
                left_header=left_header or '',
                left_rows=left_rows or [],
                right_header=right_header or '',
                right_rows=right_rows or [],
                left_header_bg=left_header_bg,
                right_header_bg=right_header_bg,
                col_ratio=col_ratio,
                gutter=gutter,
                label_width=label_width
            )
        else:
            # LAYOUT SINGOLA COLONNA
            if not rows:
                raise ValueError("Devi fornire rows per layout singola colonna")
            
            # Header opzionale
            if header:
                self.set_fill_color(*COLORS[header_bg])
                text_color = 'text_dark' if header_bg == 'primary' else 'text_white'
                self.set_text_color(*COLORS[text_color])
                self.set_font(self.font_family, 'B', 9)
                
                y_pos = self.get_y()
                x_pos = self.get_x()
                rect_width = self.w - self.l_margin - self.r_margin
                
                self.rounded_rect(x_pos, y_pos, rect_width, 7, 2, style='F')
                self.cell(0, 7, header, border=0, align=Align.C, fill=False, 
                         new_x=XPos.LEFT, new_y=YPos.NEXT)
                self.ln(2)
                
                # Reset colors
                self.set_text_color(*COLORS['text_dark'])
                self.set_fill_color(*COLORS['bg_white'])
            
            # Griglia info
            self.add_info_grid(rows, label_width=label_width)
    
    def add_zebra_table(self, headers: List[str], rows: List[List[str]],
                       col_widths: List[float] = None,
                       aligns: List[str] = None,
                       header_bg: str = 'bg_light',
                       zebra_color: str = 'bg_light',
                       header_font_size: int = 7,
                       row_font_size: int = 7,
                       header_height: float = 6,
                       row_height: float = 5,
                       repeat_header_on_new_page: bool = True):
        """
        Tabella con zebra striping automatico usando table() nativo di fpdf2.
        Gestisce automaticamente page break e ripetizione header.
        
        Args:
            headers: Lista intestazioni colonne
            rows: Lista righe (ciascuna è lista di celle)
            col_widths: Larghezze colonne (frazione di content_width, default equidistribuite)
            aligns: Allineamenti colonne (default L per prima, C per resto)
            header_bg: Colore background header
            zebra_color: Colore righe alternate
            header_font_size: Dimensione font header
            row_font_size: Dimensione font righe
            header_height: Altezza header (ignorato, usa line_height)
            row_height: Altezza righe
            repeat_header_on_new_page: Se True, ripete l'header su ogni pagina
        """
        # Default: colonne equidistribuite
        if col_widths is None:
            col_widths = [1.0 / len(headers)] * len(headers)
        
        # Converti frazioni in larghezze assolute
        absolute_widths = [w * self.content_width for w in col_widths]
        
        # Default: prima colonna a sinistra, resto centrato
        if aligns is None:
            aligns = ['L'] + ['C'] * (len(headers) - 1)
        
        # Converti aligns per fpdf2 table (LEFT, CENTER, RIGHT)
        align_map = {'L': 'LEFT', 'C': 'CENTER', 'R': 'RIGHT'}
        text_align = tuple(align_map[a] for a in aligns)
        
        # Stile header
        headings_style = FontFace(
            emphasis='BOLD',
            fill_color=COLORS[header_bg],
            size_pt=header_font_size
        )
        
        # Usa table() nativo con zebra striping
        with self.table(
            col_widths=absolute_widths,
            text_align=text_align,
            line_height=row_height * 1.4,  # Converti altezza in line_height
            cell_fill_color=COLORS[zebra_color],
            cell_fill_mode=TableCellFillMode.ROWS,  # Alterna righe
            headings_style=headings_style,
            first_row_as_headings=True,
            repeat_headings='ON_TOP_OF_EVERY_PAGE' if repeat_header_on_new_page else 0,
            borders_layout='ALL'
        ) as table:
            # Header row
            header_row = table.row()
            for header in headers:
                header_row.cell(header)
            
            # Data rows - colora manualmente per zebra con due colori
            self.set_font_size(row_font_size)
            for idx, row_data in enumerate(rows):
                # Alterna tra zebra_color e bianco, senza bold
                row_style = FontFace(
                    fill_color=COLORS[zebra_color] if idx % 2 == 0 else COLORS['bg_white'],
                    size_pt=row_font_size
                )
                data_row = table.row()
                for datum in row_data:
                    data_row.cell(str(datum), style=row_style)
    
    def draw_horizontal_line(self, color: Tuple[int, int, int] = None, width: float = 0.5, 
                            x_start: float = None, x_end: float = None, y: float = None):
        """
        Disegna una linea orizzontale.
        
        Args:
            color: Tupla RGB per il colore (default: primary color)
            width: Spessore linea
            x_start: Coordinata X inizio (default: left margin)
            x_end: Coordinata X fine (default: right margin)
            y: Coordinata Y (default: current Y position)
        """
        if color:
            self.set_draw_color(*color)
        else:
            self.set_draw_color(*COLORS.get('primary', (0, 0, 0)))
        
        old_width = self.line_width
        self.set_line_width(width)
        
        x1 = x_start if x_start is not None else self.l_margin
        x2 = x_end if x_end is not None else (self.w - self.r_margin)
        y_pos = y if y is not None else self.get_y()
        
        self.line(x1, y_pos, x2, y_pos)
        
        # Reset
        self.set_draw_color(0, 0, 0)
        self.set_line_width(old_width)

