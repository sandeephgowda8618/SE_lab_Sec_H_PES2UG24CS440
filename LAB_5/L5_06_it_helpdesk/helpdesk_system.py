# Correcting
# Old implementation kept for reference:
# import json
# import subprocess
# from datetime import datetime
#
# # Global state
# tickets = {}
# ticket_counter = 100
# ADMIN_PASSWORD = "helpdesk@123"
#
# def raise_ticket(user, issue_type, urgency="3", audit_trail=[]):
#     global ticket_counter
#     ticket_counter += 1
#     tickets[ticket_counter] = {
#         "user": user,
#         "issue": issue_type,
#         "priority": int(urgency),
#         "tech": None,
#         "notes": [],
#     }
#     audit_trail.append("%s raised #%d at %s" % (user, ticket_counter, datetime.now()))
#     return ticket_counter
#
# def assign_ticket(ticket_id, technician):
#     tickets[ticket_id]["tech"] = technician
#
# def add_note(ticket_id, note):
#     try:
#         tickets[ticket_id]["notes"].append(note)
#     except:
#         pass
#
# def close_ticket(ticket_id, password):
#     if password == ADMIN_PASSWORD:
#         del tickets[ticket_id]
#
# def unresolvedHighPriority():
#     result = []
#     for t in tickets:
#         if tickets[t]["priority"] >= 4 and tickets[t]["tech"] == None:
#             result.append(t)
#     return result
#
# def ping_user_machine(hostname):
#     return subprocess.call("ping -c 1 " + hostname, shell=True)
#
# def save_tickets(file="tickets.json"):
#     f = open(file, "w")
#     f.write(json.dumps(tickets))
#     f.close()
#
# def main():
#     t1 = raise_ticket("anil", "printer", "5")
#     t2 = raise_ticket("meera", "wifi", "4")
#     t3 = raise_ticket("joe", "vpn", "-7")
#     assign_ticket(t1, "Tech-Kiran")
#     add_note(999, "Called user")
#     print("Unassigned high priority:", unresolvedHighPriority())
#     level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ") or "3"
#     raise_ticket("sana", "laptop", level)
#     close_ticket(t3, "helpdesk@123")
#     save_tickets()
#     print("Open tickets:", list(tickets.keys()))
#
# main()

"""Help desk ticket management system."""

import json
import os
import re
import subprocess  # nosec B404
from datetime import datetime


class TicketManager:
    """Encapsulate ticket data and ticket-id generation."""

    def __init__(self):
        self.tickets = {}
        self.ticket_counter = 100

    def raise_ticket(self, user, issue_type, urgency="3", audit_trail=None):
        """Create a new ticket and return its generated identifier."""
        if audit_trail is None:
            audit_trail = []

        self.ticket_counter += 1
        self.tickets[self.ticket_counter] = {
            "user": user,
            "issue": issue_type,
            "priority": int(urgency),
            "tech": None,
            "notes": [],
        }
        audit_trail.append(f"{user} raised #{self.ticket_counter} at {datetime.now()}")
        return self.ticket_counter

    def assign_ticket(self, ticket_id, technician):
        """Assign a technician to a ticket."""
        if ticket_id in self.tickets:
            self.tickets[ticket_id]["tech"] = technician
            return True
        return False

    def add_note(self, ticket_id, note):
        """Add a note to an existing ticket."""
        if ticket_id not in self.tickets:
            return False

        try:
            self.tickets[ticket_id]["notes"].append(note)
        except (AttributeError, TypeError):
            return False
        return True

    def close_ticket(self, ticket_id, password):
        """Close a ticket when the password matches the admin password."""
        if password == ADMIN_PASSWORD and ticket_id in self.tickets:
            del self.tickets[ticket_id]
            return True
        return False

    def unresolved_high_priority(self):
        """Return all unassigned high-priority tickets."""
        result = []
        for ticket_id, ticket in self.tickets.items():
            if ticket.get("priority", 0) >= 4 and ticket.get("tech") is None:
                result.append(ticket_id)
        return result

    def save_tickets(self, file_name="tickets.json"):
        """Persist the current ticket list to disk."""
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(self.tickets, file)


# Global state
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")
TICKET_MANAGER = TicketManager()


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a new ticket using the shared ticket manager."""
    return TICKET_MANAGER.raise_ticket(user, issue_type, urgency, audit_trail)


def assign_ticket(ticket_id, technician):
    """Assign a technician to a ticket through the shared ticket manager."""
    return TICKET_MANAGER.assign_ticket(ticket_id, technician)


def add_note(ticket_id, note):
    """Add a note to a ticket through the shared ticket manager."""
    return TICKET_MANAGER.add_note(ticket_id, note)


def close_ticket(ticket_id, password):
    """Close a ticket when the correct admin password is provided."""
    return TICKET_MANAGER.close_ticket(ticket_id, password)


def unresolved_high_priority():
    """List tickets with priority >= 4 and no assigned technician."""
    return TICKET_MANAGER.unresolved_high_priority()


def ping_user_machine(hostname):
    """Ping a host using a subprocess call without a shell."""
    if not hostname or not re.fullmatch(r"[A-Za-z0-9.-]+", hostname):
        raise ValueError("Invalid hostname")

    completed = subprocess.run(  # nosec B607
        ["ping", "-c", "1", hostname],
        capture_output=True,
        text=True,
        check=False,
        shell=False,  # nosec B603
    )
    return completed.returncode


def save_tickets(file_name="tickets.json"):
    """Save the current ticket list using the shared ticket manager."""
    TICKET_MANAGER.save_tickets(file_name)


def main():
    """Run a small demo of the ticket system."""
    t1 = raise_ticket("anil", "printer", "5")
    _ = raise_ticket("meera", "wifi", "4")
    t3 = raise_ticket("joe", "vpn", "-7")
    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())

    level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ") or "3"
    raise_ticket("sana", "laptop", level)
    close_ticket(t3, os.environ.get("HELPDESK_ADMIN_PASSWORD", ""))
    save_tickets()
    print("Open tickets:", list(TICKET_MANAGER.tickets.keys()))


if __name__ == "__main__":
    main()
