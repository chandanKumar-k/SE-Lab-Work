[1mdiff --git a/fishing/game/fish.py b/fishing/game/fish.py[m
[1mindex c6bea2c..009501a 100644[m
[1m--- a/fishing/game/fish.py[m
[1m+++ b/fishing/game/fish.py[m
[36m@@ -28,3 +28,27 @@[m [mclass Fish:[m
             int(self.x - self.width / 2), int(self.y - self.height / 2),[m
             self.width, self.height,[m
         )[m
[32m+[m[32mclass SlowFish(Fish):[m
[32m+[m[32m    def __init__(self, x, y):[m
[32m+[m[32m        super().__init__([m
[32m+[m[32m            x=x,[m
[32m+[m[32m            y=y,[m
[32m+[m[32m            speed=2,[m
[32m+[m[32m            width=40,[m
[32m+[m[32m            height=20,[m
[32m+[m[32m            point_value=5,[m
[32m+[m[32m            color=(80, 180, 220)[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m
[32m+[m[32mclass FastFish(Fish):[m
[32m+[m[32m    def __init__(self, x, y):[m
[32m+[m[32m        super().__init__([m
[32m+[m[32m            x=x,[m
[32m+[m[32m            y=y,[m
[32m+[m[32m            speed=5,[m
[32m+[m[32m            width=28,[m
[32m+[m[32m            height=14,[m
[32m+[m[32m            point_value=20,[m
[32m+[m[32m            color=(220, 80, 80)[m
[32m+[m[32m        )[m
[1mdiff --git a/fishing/game/game_engine.py b/fishing/game/game_engine.py[m
[1mindex 650310d..e7df82e 100644[m
[1m--- a/fishing/game/game_engine.py[m
[1m+++ b/fishing/game/game_engine.py[m
[36m@@ -10,7 +10,7 @@[m [mgame/catch.py) that Task 1 asks you to fix.[m
 """[m
 [m
 from game.hook import Hook, IDLE[m
[31m-from game.fish import Fish[m
[32m+[m[32mfrom game.fish import SlowFish, FastFish[m
 from game.catch import check_catch[m
 from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y[m
 [m
[36m@@ -19,10 +19,11 @@[m [mclass GameEngine:[m
     def __init__(self):[m
         self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)[m
         self.fish_list = [[m
[31m-            Fish(x=100, y=180, speed=2, point_value=10, color=(80, 180, 220)),[m
[31m-            Fish(x=400, y=280, speed=-2, point_value=10, color=(80, 180, 220)),[m
[31m-            Fish(x=250, y=380, speed=3, point_value=10, color=(80, 180, 220)),[m
[31m-        ][m
[32m+[m[32m    SlowFish(x=100, y=180),[m
[32m+[m[32m    FastFish(x=400, y=280),[m
[32m+[m[32m    SlowFish(x=250, y=350),[m
[32m+[m[32m    FastFish(x=550, y=230),[m
[32m+[m[32m][m[41m   [m
         self.hooked_fish = None[m
         self.score = 0[m
 [m
