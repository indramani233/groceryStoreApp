from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from extensions import db

from forms.product_forms import ProductForm
from models.category import Category
from models.product import Product
from celery_tasks.export import export_product_details
from celery_tasks import export

store_manager_bp = Blueprint('store_manager', __name__)

@store_manager_bp.route('/store_manager/dashboard')
def store_manager_dashboard():
    #categories = Category.query.all()
    categories = Category.query.filter_by(approval_required=False).all()
    products_by_category = {}
    
    # Fetch products categorized by each category
    for category in categories:
        products = Product.query.filter_by(category_id=category.id).all()
        products_by_category[category.name] = products

    form = ProductForm()  # Create an instance of the form
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    return render_template('store_manager_dashboard.html', categories=categories, products_by_category=products_by_category, form=form)



@store_manager_bp.route('/store_manager/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        cost = float(request.form.get('cost'))  # Assuming cost is sent as a string
        category_id = int(request.form.get('category.id'))  # Assuming you have category_id in the form
        quantity_available = int(request.form.get('quantity_available'))

        product = Product(title=title, description=description, cost=cost, category_id=category_id, quantity_available=quantity_available)
        db.session.add(product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('store_manager.store_manager_dashboard'))  # Redirect to the dashboard after adding the product

    #return redirect(url_for('store_manager.store_manager_dashboard'))
    #return render_template('store_manager_dashboard.html', form=form)

@store_manager_bp.route('/store_manager/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        # Remove the product from the database
        db.session.delete(product)
        db.session.commit()

        flash('Product removed successfully!', 'success')
        return redirect(url_for('store_manager.store_manager_dashboard'))


# @store_manager_bp.route('/store_manager/products')
# def manage_products():
#     # Fetch all products
#     products = Product.query.all()
#     return render_template('store_manager_dashboard.html', products=products)



# from models.category import Category


# @store_manager_bp.route('/categories')
# def view_categories():
#     categories = Category.query.all()
#     return render_template('store_manager_dashboard.html', categories=categories)

@store_manager_bp.route('/store_manager/add_category', methods=['POST'])
def add_category():
    category_id = request.form.get('category_id')
    category_name = request.form.get('category_name')

    # Check if category already exists
    existing_category = Category.query.filter_by(id=category_id).first()
    if existing_category:
        flash('Category ID already exists', 'error')
        return redirect(url_for('store_manager.store_manager_dashboard'))

    # Create and add a new category
    new_category = Category(id=category_id, name=category_name, approval_required=True)
    db.session.add(new_category)
    db.session.commit()

    flash('Sent for approval: New category request', 'info')
    return redirect(url_for('store_manager.store_manager_dashboard'))


@store_manager_bp.route('/store_manager/remove_category/<int:category_id>', methods=['POST'])
def remove_category(category_id):
    # Check if the category exists
    category_to_remove = Category.query.get(category_id)
    if not category_to_remove:
        flash('Category does not exist', 'error')
        return redirect(url_for('store_manager.store_manager_dashboard'))

    # Mark the category for removal and send for admin approval
    category_to_remove.approval_required = True
    db.session.commit()

    flash('Sent for approval: Category removal request', 'info')
    return redirect(url_for('store_manager.store_manager_dashboard'))

@store_manager_bp.route('/export_products', methods=['POST'])
def export_products():
    try:
        # Trigger the Celery task to export product details
        export_product_details()
        #export_product_details.delay()
        #export_product_details.apply_async(countdown=5) 
        # Notify the Store Manager about the task initiation
        flash('Product export initiated. You will be notified upon completion.', 'success')
    except Exception as e:
        # Handle any errors that might occur during task execution
        flash('Error occurred while exporting products.', 'error')
    
    return redirect(url_for('store_manager.store_manager_dashboard'))
    #return redirect(url_for('store_manager.store_manager_dashboard')) , 1  # Redirect to the dashboard or appropriate page


from flask import render_template, send_file
from utils.pdf_reporting import generate_report
#from celery_tasks.export import rows
my_report_data = export_product_details

# Your Flask route handling the report generation
@store_manager_bp.route('/generate_report', methods=['GET'])
def generate_report_view():
    # Fetch report content or render HTML template
    content = render_template('report_template.html', data=my_report_data)

    # Check the user's preferred format (can come from a form input or query parameter)
    format_type = request.args.get('format', 'html')

    if format_type not in ['html', 'pdf']:
        return "Invalid format type. Please choose between HTML and PDF."

    # Generate the report based on user preference
    if format_type == 'pdf':
        file_path = 'path_to_save_pdf/report.pdf'
        generate_report(content, file_path, 'pdf')
        return send_file(file_path, as_attachment=True)

    # Return HTML content for viewing in the browser
    return content


@store_manager_bp.route('/logout')
def logout():
    # Clear the session for the store manager
    session.clear()
    # Redirect to the login page or any other page after logout
    return redirect(url_for('auth.store_manager_login'))  # Replace 'login' with your login route