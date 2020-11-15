
# @app.route('/', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':

#         total_file = len(os.listdir(directory))
#         file = request.files['file']
#         os.rename(directory)

#     return render_template('form.html')
# # @app.route('/profile/<int:id>')
# # def profile_id(id):
# #     return render_template('profile.html', id=id)

# if __name__ == '__main__':
#     app.run(debug=True)