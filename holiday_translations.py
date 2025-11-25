
def holiday_translation_spanish(holiday_name: str):
    """Translate holiday name from English to Spanish."""
    
    holiday_name_spanish = {
    "New Year's Day": "Año Nuevo",
    "Martin Luther King, Jr. Day": "Día de Martin Luther King Jr.",
    "Washington's Birthday": "Día de Washington (Día de los Presidentes)",
    "Memorial Day": "Día de los Caídos",
    "Juneteenth National Independence Day": "Día de la Independencia Nacional Juneteenth",
    "Independence Day": "Día de la Independencia",
    "Labor Day": "Día del Trabajo",
    "Columbus Day": "Día de la Raza",
    "Veterans Day": "Día de los Veteranos",
    "Thanksgiving Day": "Día de Acción de Gracias",
    "Christmas Day": "Navidad"
}

    return holiday_name_spanish.get(holiday_name, holiday_name) # Return the original name if not found in the dictionary

