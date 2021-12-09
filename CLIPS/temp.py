import clips
if __name__ == '__main__':
    DEFTEMPLATE_STRING = """
    (deftemplate person
      (slot name (type STRING))
      (slot surname (type STRING))
      (slot birthdate (type SYMBOL)))
    """

    environment = clips.Environment()

    # load constructs into the environment from a file
    environment.load('genearted_clips.clp')

    # define a fact template
    environment.build(DEFTEMPLATE_STRING)

    # retrieve the fact template
    template = environment.find_template('person')

    # assert a new fact through its template
    fact = template.assert_fact(name='John',
                                surname='Doe',
                                birthdate=clips.Symbol('01/01/1970'))

    # fact slots can be accessed as dictionary elements
    assert fact['name'] == 'John'

    # execute the activations in the agenda
    environment.run()