# Kill Them All
import random


class Player:
    def __init__(self):
        self.hp = 35
        self.energy = 5
        self.lvl = 1
        self.soft_dmg = 0
        self.hard_dmg = []
        self.enemies_killed = 0
        self.recalculate_dmg()

    def stats(self):
        print('=' * 20)
        print('HP:', self.hp)
        print('ENERGY:', self.energy)
        print('LEVEL:', self.lvl)
        print('ENEMIES KILLED: ', self.enemies_killed)
        input('\n\t<enter>')

    def level_up(self):
        self.lvl += 1
        self.energy += 1
        self.hp += 1
        self.recalculate_dmg()

    def recalculate_dmg(self):
        self.soft_dmg = self.lvl + 1
        self.hard_dmg = [self.lvl + 2, self.lvl + 3, self.lvl + 4]

    def display_battle_menu(self):
        print('=' * 20)
        print('<1> BASIC, damage = [{}]\n<2> HARD, dmg = [{}], it costs energy\n<3> Smile in his face'.format(self.soft_dmg, self.hard_dmg))

    def get_attack_type(self):
        while True:
            n = input()
            if n == '1' or n == '2' or n == '3':
                if n == '2':
                    if self.energy > 0:
                        return n
                    else:
                        print('Not enough energy.')
                else:
                    return n

    def attack(self):
        self.display_battle_menu()
        attack_type = self.get_attack_type()
        dmg = 0
        if attack_type == '1':
            print('\nSmashed!')
            dmg = self.soft_dmg
        elif attack_type == '2':
            hard_attack = random.randint(0, len(self.hard_dmg) - 1)
            dmg = self.hard_dmg[hard_attack]
            self.energy -= 2
            msg = ''
            if hard_attack == 0:
                msg += '\nMeteoroid!'
            elif hard_attack == 1:
                msg += '\nSupernova!!'
            elif hard_attack == 2:
                msg += '\nBIG BANG!!!'
            msg += ' - dealt [{}]'.format(self.hard_dmg[hard_attack])
            print(msg)
        elif attack_type == '3':
            print('\t:) - Energy +2\n')
            self.energy += 2
        return dmg


class Oscar:
    def __init__(self, name='', hp=0, dmg=tuple()):
        self.name = name
        self.hp = hp
        self.dmg = dmg

    def init(self):
        print('\n{} - {}HP - has appeared!'.format(self.name, self.hp))

    def display_hp(self):
        print('{} has {} hp left.'.format(self.name, self.hp))

    def attack(self):
        raise NotImplemented

    def dead(self):
        print('{} has been mutilated!'.format(self.name))


class MicroOscar(Oscar):
    def __init__(self):
        super().__init__(name='MicroOscar', hp=8, dmg=(0, 1, 1, 2))

    def attack(self):
        dmg = random.choice(self.dmg)
        msg = ''
        if dmg == 0:
            msg += 'He blamed you.'
        elif dmg == 1:
            msg += 'WOW, he is really pissed on you!'
        elif dmg == 2:
            msg += 'He runs around and accidentally crushes you...'
        msg += ' - he does [{}] damage.'.format(dmg)
        print(msg)
        return dmg


class CommonOscar(Oscar):
    def __init__(self):
        super().__init__(name='CommonOscar', hp=14, dmg=(2, 2, 3, 4))

    def attack(self):
        dmg = random.choice(self.dmg)
        msg = ''
        if dmg == 2:
            msg += 'He bites you!'
        elif dmg == 3:
            msg += 'He punched your face!'
        elif dmg == 4:
            msg += 'He has just kicked your face!'
        msg += ' - he does [{}] damage.'.format(dmg)
        print(msg)
        return dmg


class SupraOscar(Oscar):
    def __init__(self):
        super().__init__(name='SupraOscar', hp=20, dmg=(4, 5, 5, 6))
        print('\nPut your hands up...!')

    def attack(self):
        dmg = random.choice(self.dmg)
        msg = ''
        if dmg == 4:
            msg += 'He is throwing a banana!'
        elif dmg == 5:
            msg += 'He is trying a mad assault!'
        elif dmg == 6:
            msg += 'WTF is that!?!?!?'
        msg += ' - he does [{}] damage.'.format(dmg)
        print(msg)
        return dmg


def battle(player, enemy):
    enemy.init()
    while player.hp > 0 and enemy.hp > 0:
        enemy.hp -= player.attack()
        enemy.display_hp()
        if enemy.hp <= 0:
            enemy.dead()
            player.enemies_killed += 1
            player.level_up()
            break
        else:
            player.hp -= enemy.attack()


def generate_enemy(lvl):
    enemy_prob = (1, 1, 1, 2, 2, 3)
    enemy = random.choice(enemy_prob)
    if enemy == 1:
        return MicroOscar()
    elif enemy == 2:
        return CommonOscar()
    elif enemy == 3:
        if lvl > 4:
            return SupraOscar()
        else:
            print('\nSuicide now! Supra Oscar appears. Your level is too low, you should run.')


def get_action():
    print('=' * 20)
    print('<1> Fight\n<5> Stats\n<8> Surrender')
    while True:
        n = input()
        if n == '1' or n == '5' or n == '8':
            return n
        else:
            print('Invalid command.')


def end(killed):
    print('\nYou exterminated [{}] Oscars!'.format(killed))
    input('Hard job.\n\n THANKS FOR PLAYING!\n')


def main():
    print('- Welcome to Exterminate All Oscars -\n')
    player = Player()
    while player.enemies_killed < 31:
        option = get_action()
        if option == '1':
            enemy = generate_enemy(player.lvl)
            if enemy:
                battle(player, enemy)
                if player.hp <= 0:
                    print('\n-DEATH-\n\nOscar eats your brain...')
                    end(player.enemies_killed)
                    break
        elif option == '5':
            player.stats()
        elif option == '8':
            end(player.enemies_killed)
            break
    else:
        input('\nAmazing! You have eradicated all Oscars species!')
        end(player.enemies_killed)


if __name__ == '__main__':
    main()
