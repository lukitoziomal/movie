import pandas as pd
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from movies.scraper import scrap
#'C:\\Users\luxxx\Desktop\jupiter\movies.csv'
data = pd.read_csv('movies.csv')
df = pd.DataFrame(data)
Window.size = (400, 700)
genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
          'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Reality-TV',
          'Romance', 'Sci-Fi', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']
boxes = []


class MainScreen(Screen):
    pass


class FindScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.year1 = 1899
        self.year2 = 2020
        self.rating = 1.5
        self.genres_conditions = []

    def roll(self):
        fin = self.find()
        sel = scrap(list(fin.tconst)[0])
        return fin, sel

    def find(self):
        years = df[(df.startYear > self.year1) & (df.startYear < self.year2)]
        if len(self.genres_conditions) != 0:
            for arg in self.genres_conditions:
                years = years[years.genres.str.contains(arg)]
        return years.sample()

    def check(self):
        for box in boxes:
            if box.active:
                self.genres_conditions.append(box.text)
        print(self.genres_conditions, self.year1, self.year2, self.rating)

    def searcher(self):
        final, selected = self.roll()
        run = True
        i = 1
        while run:
            na = True
            while na:
                if selected.total_ratings == 'N/A':
                    final, selected = self.roll()
                else:
                    rat = ''
                    for digit in selected.total_ratings:
                        if digit != ',':
                            rat += digit
                    selected.total_ratings = int(rat)
                    na = False
                    break
            if selected.total_ratings < 500 or float(selected.rating) < self.rating:
                final, selected = self.roll()
            else:
                run = False
                break

        self.manager.get_screen('result').ids.poster.source = selected.poster
        movie_title = str(list(final.primaryTitle)[0])
        if len(movie_title) > 17:
            new = ''
            liner = True
            for word in movie_title.split(' '):
                if liner:
                    if len(new) >= 17:
                        new += '\n' + word
                        liner = False
                    else:
                        new += word + ' '
                else:
                    new += word + ' '
            movie_title = new
        self.manager.get_screen('result').ids.title.text = movie_title
        self.manager.get_screen('result').ids.details.text = '{} mins, ({}) {}, {}'.format(str(list(final.runtimeMinutes)[0]),
                                                                                      str(list(final.startYear)[0]),
                                                                                      selected.country, selected.lang)
        self.manager.get_screen('result').ids.ratings.text = '{} based on {} votes'.format(selected.rating, selected.total_ratings)
        self.manager.get_screen('result').ids.cast.text = 'Director: {}\nWriter: {}\nStars: {}'.format(selected.director,
                                                                                                          selected.writer,
                                                                                                          selected.stars)
        if len(selected.overview) > 50:
            new = ''
            liner = True
            liner2 = False
            liner3 = False
            for word in selected.overview.split(' '):
                if liner:
                    if len(new) > 50:
                        new += '\n' + word
                        liner = False
                        liner2 = True
                    else:
                        new += word + ' '
                elif liner2:
                    if len(new) > 100:
                        new += '\n' + word
                        liner2 = False
                        liner3 = True
                    else:
                        new += word + ' '
                elif liner3:
                    if len(new) > 150:
                        new += '\n' + word
                        liner3 = False
                    else:
                        new += word + ' '
                else:
                    new += word + ' '
            selected.overview = new

        self.manager.get_screen('result').ids.overview.text = selected.overview

        self.genres_conditions = []


class ResultScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


class Boxes(GridLayout):
    def __init__(self, **kwargs):
        super(Boxes, self).__init__(**kwargs)
        self.cols = 6
        self.row_default_height = 3
        for genre in genres:
            self.add_widget(Label(text=genre, width=40))
            self.active = CheckBox(active=False)
            self.active.text = genre
            self.add_widget(self.active)
            boxes.append(self.active)


class Movie(App):
    def build(self):
        return Builder.load_file('config.kv')


if __name__ == '__main__':
    Movie().run()



