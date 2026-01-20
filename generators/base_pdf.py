from typing import Literal, List, Dict, Any, Optional, Sequence, Tuple
from fpdf import FPDF
from fpdf.enums import XPos, YPos, Align
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
