# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCheckEligibility(Action):

    def name(self) -> str:
        return "action_check_eligibility"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> List[Dict[Text, Any]]:

        is_omogeneis = tracker.get_slot("is_omogeneis")
        is_child = tracker.get_slot("is_child")
        is_spouse = tracker.get_slot("is_spouse")

        if is_omogeneis == "yes":
            if is_child == "yes":
                dispatcher.utter_message(text="Ως τέκνο ομογενούς, δικαιούσαι Ε.Δ.Τ.Ο. υπό προϋποθέσεις.")
            elif is_spouse == "yes":
                dispatcher.utter_message(text="Ως σύζυγος ομογενούς, μπορεί να δικαιούσαι Ε.Δ.Τ.Ο. υπό προϋποθέσεις (ανήλικα τέκνα, χηρεία κ.λπ.).")
            else:
                dispatcher.utter_message(text="Δικαιούσαι Ε.Δ.Τ.Ο. ως ομογενής από την Αλβανία ή την πρώην ΕΣΣΔ.")
        elif is_omogeneis == "no":
            dispatcher.utter_message(text="Δυστυχώς, αν δεν έχεις ομογενειακή ιδιότητα, δεν δικαιούσαι Ε.Δ.Τ.Ο.")
        else:
            dispatcher.utter_message(text="Δεν γνωρίζω αν είστε ομογενής. Μπορείτε να απαντήσετε Ναι ή Όχι;")
        return []


class ActionProvideDocuments(Action):

    def name(self) -> str:
        return "action_provide_documents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_child = tracker.get_slot("is_child")
        is_spouse = tracker.get_slot("is_spouse")
        is_widow = tracker.get_slot("is_widow")

        docs_child = (
            "Για την έκδοση Ε.Δ.Τ.Ο. ανηλίκου απαιτούνται:\n"
            "- Αίτηση\n"
            "- Διαβατήριο ανηλίκου\n"
            "- Πιστοποιητικό γέννησης\n"
            "- Φωτογραφίες\n"
            "- Ε.Δ.Τ.Ο. του γονέα\n"
            "- Αποδεικτικό γονικής μέριμνας"
        )

        docs_widow = (
            "Για χήρα/χήρο ομογενούς απαιτούνται:\n"
            "- Διαβατήριο\n"
            "- Πιστοποιητικό γάμου\n"
            "- Ληξιαρχική πράξη θανάτου του ομογενούς συζύγου\n"
            "- Φωτογραφίες\n"
            "- Βεβαίωση ελληνικής καταγωγής"
        )

        docs_spouse = (
            "Για αλλοδαπό σύζυγο ομογενούς απαιτούνται:\n"
            "- Αίτηση\n"
            "- Διαβατήριο\n"
            "- Πιστοποιητικό γάμου\n"
            "- Ε.Δ.Τ.Ο. του ομογενούς συζύγου\n"
            "- Φωτογραφίες\n"
            "- Πιστοποιητικά οικογενειακής κατάστασης"
        )

        docs_adult = (
            "Για ομογενείς ενήλικες:\n"
            "- Αίτηση\n"
            "- Διαβατήριο\n"
            "- Πιστοποιητικό γέννησης\n"
            "- Έγγραφα ελληνικής καταγωγής (π.χ. εκκλησιαστικά ή εκπαιδευτικά)\n"
            "- Φωτογραφίες"
        )

        if is_child == "yes":
            dispatcher.utter_message(text=docs_child)
        elif is_widow == "yes":
            dispatcher.utter_message(text=docs_widow)
        elif is_spouse == "yes":
            dispatcher.utter_message(text=docs_spouse)
        elif is_child == "no" and is_spouse == "no":
            dispatcher.utter_message(text=docs_adult)
        else:
            dispatcher.utter_message(text=(
                "Δεν έχω αρκετές πληροφορίες για να προσδιορίσω τα δικαιολογητικά.\n"
                "Η αίτηση αφορά τέκνο ομογενούς;"
            ))

        return []
