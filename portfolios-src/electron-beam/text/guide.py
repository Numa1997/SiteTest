"""The reading guide of project 07 (the four boxes at the top of the page). Written by the finisher, 9 November 2026. HTML with $maths$."""
GUIDE = {
    'shows': ('One electron’s way from a sharp metal tip to a measured line width on a wafer, in ten short chapters. The tip emits it '
              '(chapter 2), and fields accelerate and focus it (chapters 1, 3, 4). The optics squeeze it into a probe a few nanometres wide '
              '(chapter 5). It scatters inside the wafer and sends back the signal (chapter 6), and a width is read from that signal with '
              'a known precision (chapter 7). Chapter 8 joins the stages into one machine; chapter 9 gathers the threads. Each chapter starts '
              'from an everyday picture, derives its formulas, and ends with a simulation whose sliders are the symbols of the formulas. '
              'Chapters 0 and 9 can be read alone; the rest build on each other.'),
    'models': ('Newton’s and Lorentz’s laws for a charge in fields, with relativity where it matters. Field emission by tunnelling, '
               'and brightness and its conservation. A magnetic lens with Glaser’s bell-shaped field, traced ray by ray. The four blurs of a '
               'probe and the best beam angle. The scattering of electrons in silicon, aluminium, copper and gold, by a Monte Carlo '
               'simulation. The shot noise of counting and the precision of an edge. And the chain of all these, with a sensitivity '
               'table and a tolerance study.'),
    'leaves_out': ('Real pole-piece fields (the lens field is an analytic model, and there is no field solver), aberration correctors, '
                   'misalignment and coma, the interaction of beam electrons with each other, charging of insulators, resist damage, '
                   'three-dimensional scattering in a real line, and any detail of a commercial instrument. Where a model is used outside '
                   'its range (low voltage on heavy elements, for example), the chapter says so and shows the gap to measurements. '
                   'Spreads and specifications in chapter 8 are stated assumptions.'),
    'numbers': ('SI units throughout; constants from CODATA 2018. Every number in the text is computed by the project’s code, not typed. '
                'Every browser module except the one of chapter eight, which only chains the others, has an independent Python twin '
                'that must agree with it. The derivations are checked symbolically, and published data (stopping powers, backscattering '
                'measurements, secondary-electron yields, lens coefficients) are shown beside the model with their source. Each chapter '
                'ends with its table of checks. Every chapter was also read by two independent reviewers, and what they found is '
                'recorded in the project’s audit notes.'),
}
