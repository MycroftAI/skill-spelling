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

from adapt.intent import IntentBuilder
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill


class SpellingSkill(OVOSSkill):
    SEC_PER_LETTER = 0.9  # based on the Mark 1 scrolling speed
    LETTERS_PER_SCREEN = 7.0  # based on the Mark 1 screen size

    @intent_handler(IntentBuilder("").require("Spell").require("Word"))
    def handle_spell(self, message):
        word = message.data.get("Word")
        spelled_word = '; '.join(word).upper()

        # Pause mouth shapes appearing on screen for at least enough time
        # for the word to scroll by on the Mark 1 screen.  Pad with blanks
        # to prevent re-starting the scroll action if the timing is slightly
        # off.
        self.enclosure.deactivate_mouth_events()
        self.enclosure.mouth_text(word + "          ")

        self.speak(spelled_word, wait=True)

        # allow mouth movements again
        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()
