from jinja2 import Environment, FileSystemLoader

env = Environment(loader = FileSystemLoader('./'))
template = env.get_template('template.html') # Change to template.html.j2 when done

output = template.render(
  name = 'Test',
  test2 = 'Test2'
)

with open("weather.html", "w") as html:
  html.write(output)


# print(output)