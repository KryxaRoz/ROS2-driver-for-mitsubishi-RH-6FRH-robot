#!/usr/bin/env python3
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from scara_msgs.action import Task
import threading

threading.Thread(target=lambda: rclpy.init()).start()

action_client = ActionClient(Node("scara_alexa"), Task, "task_server")

app = Flask(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hi there sweetie. What can i do for you today?"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
            
        # goal = Task.Goal()
        # goal.task_number = 0
        # action_client.send_goal_async(goal)
        return handler_input.response_builder.response
    
class HomingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HomingIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Moving to my home position sweetie"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("powrot do domu", speech_text)).set_should_end_session(
            True)
        goal = Task.Goal()
        goal.task_number = 0
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response
    
class TurnRightIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TurnRightIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hmmm if you say so. Well I'm just a robot after all darling"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("skrecanie w prawo", speech_text)).set_should_end_session(
            True)
        goal = Task.Goal()
        goal.task_number = 1
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response
    
class TurnLeftIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TurnLeftIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Of course darling. Is there anything else you would like me to do?"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("skrecanie w lewo", speech_text)).set_should_end_session(
            True)
        goal = Task.Goal()
        goal.task_number = 2
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response
    
class SleepIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SleepIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Stupid human. You know that robots cannot sleep? I can just make myself in a standby mode."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("spanko", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response
    
class WakeUpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WakeUpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "I'm still here darling"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("wstawanko", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Dear human, you have to use proper commands in order to make me work for you"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
    
skill_builder = SkillBuilder()
skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(HomingIntentHandler())
skill_builder.add_request_handler(TurnRightIntentHandler())
skill_builder.add_request_handler(TurnLeftIntentHandler())
skill_builder.add_request_handler(SleepIntentHandler())
skill_builder.add_request_handler(WakeUpIntentHandler())
skill_builder.add_exception_handler(AllExceptionHandler())

skill_adapter = SkillAdapter(
    skill=skill_builder.create(), skill_id="amzn1.ask.skill.3a221c2e-67a5-451c-b504-38a6713214c9", app=app)

@app.route("/")
def invoke_skill():
    return skill_adapter.dispatch_request()


skill_adapter.register(app=app, route="/")

if __name__ =="__main__":
        app.run()