# Copyright 2018 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.audio import wait_while_speaking


class SpellingSkill(MycroftSkill):
    SEC_PER_LETTER = 0.9         # based on the Mark 1 scrolling speed
    LETTERS_PER_SCREEN = 7.0     # based on the Mark 1 screen size

    def __init__(self):
        super(SpellingSkill, self).__init__(name="SpellingSkill")

    @intent_handler(IntentBuilder("").require("Spell").require("Word"))
    def handle_spell(self, message):
        word = message.data.get("Word")
        spelled_word = '. '.join(word).upper()

        self.enclosure.deactivate_mouth_events()
        self.speak(spelled_word)

        # Pause mouth shapes appearing on screen for at least enough time
        # for the word to scroll by on the Mark 1 screen.  Pad with blanks
        # to prevent re-starting the scroll action if the timing is slightly
        # off.

        # TODO: Add mouth_text(word, wrap_at_end=False) parameter and get rid
        #       of the need for deactivate_mouth_events() -- or at least handle
        #       at the Enclosure level.
        self.enclosure.mouth_text(word+"          ")
        time.sleep(self.LETTERS_PER_SCREEN + len(word) * self.SEC_PER_LETTER)
        wait_while_speaking()

        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()


def create_skill():
    return SpellingSkill()
