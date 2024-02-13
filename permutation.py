# def shoot(self):
#     if self.cool_down_counter == 0:
#         laser = Laser(self.x + 15, self.y, self.laser_img)
#         self.lasers.append(laser)
#         self.cool_down_counter = 1
#         laser_music = mixer.Sound('laser.wav')
#         laser_music.play()
#
#
# def move_lasers(self, vel, objs):
#     self.cooldown()
#
#     for laser in self.lasers:
#         laser.move(vel)
#         if laser.off_screen(height):
#             self.lasers.remove(laser)
#         else:
#             for obj in objs:
#                 if laser.collision(obj):
#
#                     collision_music = mixer.Sound('explosion.wav')
#                     collision_music.play()
#
#                     objs.remove(obj)
#
#                     if laser in self.lasers:
#                         self.lasers.remove(laser)
#

for _ in range(input()):
    n=int(input())
    l=[]

    if n==3:
        print("NO")
        continue
    elif n%2==0:
        print("YES")
        for i in range(n//2):
            l.append("1")
            l.append("-1")
        print(" ".join(l))
        continue

    else:
        print("YES")
        val=n//2
        for i in range(n//2):
            l.append(str(1-val))
            l.append(str(val))
        l.append(str(1-val))
        print(" ".join(l))
        continue



