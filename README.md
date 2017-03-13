# LadderiLogical

Application for creating graphical "Ladder Logic" programs. It includes compiler targeting PIC Assembly.

A program is "written" by laying out tiles representing logical functions (timers, counters etc) on a board and connecting them using red wires (relay tiles). The state of each wire is shown using green dots in real time. The application includes capability to save/open programs in a human readable format based on json (.lil)

![IMAGE](https://github.com/mikadam/LadderiLogical/blob/master/examples/screen_shot.png)

To the right of the board there are options to convert the selected tile to a different type and various tile specific options (such as configuring which way to accept IO from). Further right there is a panel allowing the user to manually interact with flags (those will be compiled to the pins on the PIC). Flags can we used to transmit the state of a wire "wirelessly" by specifying a unique text identifier. The application resolves any errors that may arise from multiple sources trying to drive the same flag

###Tile Types:

**Tile** - a "do nothing tile"  
**Relay** - A wire that conducts/transmits a signal  
**Source** - Outputs an on signal in all directions  
**Flag** - Drives a flag with the value of its input  
**Generator** - Outputs a signal depending on a flag  
**Switch** - Conducts signal when the selected flag is high (or low when inverted)  
**Counter** - Outputs high after the selected number of rising edges  
**Pulsar** - Generates a square wave of a given frequency  
**Timer** - Either ensures a pules is at least n ms long (hold mode) or delays the rising edge (and turns it into a as-short-as-possible pulse) by n ms (delay monostable)  
**Sequencer** - Drives a sequence on flags in a one-hot fashion. Move to the next flag on a rising edge  

To upload it to a PIC you need open the generated file in MPLab and  assemble it before uploading.

###Keyboard shortcuts:

<pre>
	S: <b>S</b>elect tile
	A: Place wire and <b>a</b>utomaticly determine direction
	F: Place <b>f</b>lag input tile
	H: Place switch tile and configure input/output <b>h</b>orizontaly
	X: Delete tile
	
	The arrow keys move the selection around
	
	Holding shift prevents the tool from automatically switching 
	back to the select tool after a single use
	
</pre>
	
### Building

This collection of python scipts can be converted into an Mac Application bundle using py2app. Just run `python3 setup_mac.py py2app`

Michal Adamkiewicz 2017

