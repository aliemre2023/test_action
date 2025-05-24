from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_hello_pdf(output_path="documentation/hello.pdf"):
    """
    Creates a PDF document with the title 'Hello'
    
    Args:
        output_path (str): The path where the PDF will be saved
    """
    # Create a canvas with letter size
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Get page width and height
    width, height = letter
    
    # Set font and size for the title
    c.setFont("Helvetica-Bold", 36)
    
    # Draw the title 'Hello' in the center of the page
    c.drawCentredString(width/2, height/2, "Hello")
    
    # Save the PDF
    c.save()
    
    print(f"PDF created successfully at {output_path}")

if __name__ == "__main__":
    create_hello_pdf()