import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class ReportGenerator:
    def __init__(self, user):
        self.user = user
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'CustomStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=20
        )

    def generate_pdf_report(self, start_date, end_date):
        """Generate a PDF report for the given date range"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []

        # Add title
        title = Paragraph(f"Eco-Route Analysis Report", self.styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))

        # Add date range
        date_range = Paragraph(
            f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            self.custom_style
        )
        story.append(date_range)
        story.append(Spacer(1, 20))

        # Add summary statistics
        stats = self.get_summary_statistics(start_date, end_date)
        story.extend(self.create_summary_section(stats))

        # Add charts
        story.extend(self.create_charts_section(start_date, end_date))

        # Add detailed route table
        story.extend(self.create_routes_table(start_date, end_date))

        # Build PDF
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()

        # Save to storage
        filename = f"report_{self.user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        path = default_storage.save(f"reports/{filename}", ContentFile(pdf))
        return path

    def generate_excel_report(self, start_date, end_date):
        """Generate an Excel report for the given date range"""
        routes = self.get_routes_data(start_date, end_date)
        
        # Create Excel writer
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Routes sheet
            routes_df = pd.DataFrame(routes)
            routes_df.to_excel(writer, sheet_name='Routes', index=False)

            # Summary sheet
            stats = self.get_summary_statistics(start_date, end_date)
            stats_df = pd.DataFrame([stats])
            stats_df.to_excel(writer, sheet_name='Summary', index=False)

            # Weather Impact sheet
            weather_data = self.get_weather_impact_data(start_date, end_date)
            weather_df = pd.DataFrame(weather_data)
            weather_df.to_excel(writer, sheet_name='Weather Impact', index=False)

            # Format sheets
            self.format_excel_sheets(writer)

        # Save to storage
        filename = f"report_{self.user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        path = default_storage.save(f"reports/{filename}", ContentFile(output.getvalue()))
        return path

    def get_summary_statistics(self, start_date, end_date):
        """Get summary statistics for the report"""
        from sdg9.models import Route
        routes = Route.objects.filter(
            user=self.user,
            created_at__range=(start_date, end_date)
        )

        return {
            'total_routes': routes.count(),
            'total_distance': sum(r.distance for r in routes),
            'total_fuel': sum(r.fuel_consumption for r in routes),
            'total_emissions': sum(r.carbon_emissions for r in routes),
            'avg_efficiency': sum(r.fuel_consumption/r.distance for r in routes) / routes.count() if routes else 0
        }

    def create_charts_section(self, start_date, end_date):
        """Create charts for the report"""
        story = []
        
        # Efficiency Trend Chart
        plt.figure(figsize=(8, 4))
        # ... create chart using matplotlib ...
        chart_buffer = BytesIO()
        plt.savefig(chart_buffer)
        chart_image = Image(chart_buffer)
        story.append(chart_image)
        story.append(Spacer(1, 20))

        return story

    def create_routes_table(self, start_date, end_date):
        """Create a detailed routes table"""
        routes = self.get_routes_data(start_date, end_date)
        
        # Create table data
        table_data = [['Date', 'Route', 'Distance', 'Fuel Used', 'CO2 Emissions']]
        for route in routes:
            table_data.append([
                route['date'],
                f"{route['source']} to {route['destination']}",
                f"{route['distance']:.1f} km",
                f"{route['fuel_consumption']:.1f} L",
                f"{route['carbon_emissions']:.1f} kg"
            ])

        # Create table
        table = Table(table_data)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        return [table]

    def format_excel_sheets(self, writer):
        """Format Excel sheets"""
        workbook = writer.book
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white'
        })
        
        number_format = workbook.add_format({
            'num_format': '#,##0.00'
        })

        # Format each worksheet
        for worksheet in writer.sheets.values():
            worksheet.set_column('A:Z', 15)  # Set column width
            worksheet.set_row(0, 20, header_format)  # Format header row